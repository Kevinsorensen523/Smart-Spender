from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Item
import json
import random
from django.shortcuts import get_object_or_404
import csv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

# Get All Items or Create a New Item
@api_view(['GET', 'POST'])
def items_list(request):
    if request.method == 'GET':
        items = list(Item.objects.values())
        return Response(items)

    if request.method == 'POST':
        name = request.data.get('name')
        price = request.data.get('price')
        if name and price:
            item = Item.objects.create(name=name, price=price)
            return Response({'id': item.id, 'name': item.name, 'price': item.price}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

# Get, Update, or Delete a Specific Item
@api_view(['GET', 'PUT', 'DELETE'])
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if request.method == 'GET':
        return Response({'id': item.id, 'name': item.name, 'price': item.price})

    if request.method == 'PUT':
        item.name = request.data.get('name', item.name)
        item.price = request.data.get('price', item.price)
        item.save()
        return Response({'id': item.id, 'name': item.name, 'price': item.price})

    if request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def import_csv(request):
    if request.method == 'POST' and request.FILES.get('file'):
        # Ambil file dari request
        csv_file = request.FILES['file']

        # Simpan file sementara (opsional, bisa langsung di-stream juga)
        file_path = default_storage.save('tmp/' + csv_file.name, csv_file)

        # Baca file CSV
        try:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Pastikan CSV memiliki kolom 'name' dan 'price'
                    name = row.get('name')
                    price = row.get('price')
                    if name and price:
                        Item.objects.create(name=name, price=price)

            return JsonResponse({'message': 'Data berhasil diimpor'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
@csrf_exempt
def recommendation(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            budget = float(data.get("budget", 0))
            selected_items = data.get("items", [])

            print(f"Budget received: {budget}")
            print(f"Selected items received: {selected_items}")

            items = []
            for selected in selected_items:
                item = Item.objects.filter(id=selected["id"]).first()
                if item:
                    print(f"Item found: {item.name}, Price: {item.price}")
                    items.append({
                        "id": item.id,
                        "name": item.name,
                        "price": float(item.price),
                        "priority": selected["priority"],
                    })

            print(f"Items before filtering: {items}")

            items = [item for item in items if item["price"] <= budget]
            print(f"Filtered items: {items}")

            if not items:
                return JsonResponse({
                    "recommendations": [],
                    "budget": budget,
                    "total_cost": 0,
                    "remaining_budget": budget,
                    "message": "Tidak ada barang yang dapat dibeli dengan anggaran Anda.",
                })

            def fitness(solution):
                total_cost = sum(item["price"] * qty for item, qty in solution)
                total_priority = sum(item["priority"] * qty for item, qty in solution)
                if total_cost > budget:
                    return 0
                return total_priority

            def generate_population(pop_size, items):
                population = []
                for _ in range(pop_size):
                    individual = []
                    for item in items:
                        max_qty = int(budget / item["price"]) if item["price"] <= budget else 0
                        qty = random.randint(0, max_qty) if max_qty > 0 else 0
                        individual.append((item, qty))
                    population.append(individual)
                print(f"Generated initial population of size {len(population)}")
                return population

            def mutate(individual):
                idx = random.randint(0, len(individual) - 1)
                item, qty = individual[idx]
                max_qty = int(budget / item["price"]) if item["price"] <= budget else 0
                individual[idx] = (item, random.randint(0, max_qty) if max_qty > 0 else 0)
                return individual

            def crossover(parent1, parent2):
                pivot = random.randint(1, len(parent1) - 1)
                child1 = parent1[:pivot] + parent2[pivot:]
                child2 = parent2[:pivot] + parent1[pivot:]
                return child1, child2

            population_size = 50
            generations = 100
            mutation_rate = 0.1

            population = generate_population(population_size, items)

            for generation in range(generations):
                population = sorted(population, key=fitness, reverse=True)
                next_generation = population[:10]

                while len(next_generation) < population_size:
                    parent1, parent2 = random.sample(population[:20], 2)
                    child1, child2 = crossover(parent1, parent2)
                    next_generation.append(child1)
                    next_generation.append(child2)

                for individual in next_generation:
                    if random.random() < mutation_rate:
                        mutate(individual)

                population = next_generation
                print(f"Generation {generation + 1} completed")

            best_solution = max(population, key=fitness)
            print(f"Best solution: {best_solution}")

            recommendations = []
            total_cost = 0
            for item, qty in best_solution:
                if qty > 0:
                    total_price = item["price"] * qty
                    total_cost += total_price
                    recommendations.append({
                        "id": item["id"],
                        "name": item["name"],
                        "price": item["price"],
                        "quantity": qty,
                        "total_price": total_price,
                    })

            print(f"Total cost: {total_cost}, Remaining budget: {budget - total_cost}")
            print(f"Recommendations: {recommendations}")

            return JsonResponse({
                "recommendations": recommendations,
                "budget": budget,
                "total_cost": total_cost,
                "remaining_budget": budget - total_cost,
                "message": "Rekomendasi berhasil dihasilkan" if recommendations else "Tidak ada rekomendasi yang memenuhi anggaran",
            })

        else:
            return JsonResponse({"error": "Invalid request method"}, status=405)

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({"error": str(e)}, status=500)
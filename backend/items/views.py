from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Item
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
        
def recommendation(request):
    budget = float(request.GET.get('budget', 0))
    items = list(Item.objects.values())

    # Contoh genetic algorithm sederhana
    def fitness(solution):
        total_cost = sum(item['price'] for item in solution)
        if total_cost > budget:
            return 0  # Tidak valid
        return total_cost  # Semakin tinggi total biaya yang valid, semakin baik

    def genetic_algorithm(items, budget):
        from itertools import combinations
        best_solution = []
        best_fitness = 0
        for r in range(1, len(items) + 1):
            for solution in combinations(items, r):
                score = fitness(solution)
                if score > best_fitness:
                    best_fitness = score
                    best_solution = solution
        return best_solution

    recommendations = genetic_algorithm(items, budget)
    return JsonResponse({'recommendations': recommendations})
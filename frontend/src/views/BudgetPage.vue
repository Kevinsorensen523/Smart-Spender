<template>
  <div>
    <h1>Masukkan Jumlah Uang Anda</h1>
    <form @submit.prevent="submitBudget">
      <label for="budget">Jumlah Uang:</label>
      <input
        v-model.number="budget"
        type="number"
        id="budget"
        placeholder="Jumlah uang"
        required
      />
      <button type="submit">Lanjutkan</button>
    </form>

    <div v-if="items.length > 0">
      <h2>Pilih Barang dan Prioritas</h2>
      <ul>
        <li v-for="item in items" :key="item.id">
          <label>
            <input type="checkbox" v-model="selectedItems" :value="item" />
            {{ item.name }} - Rp {{ item.price }}
          </label>
          <input
            v-if="selectedItems.includes(item)"
            v-model.number="item.priority"
            type="number"
            placeholder="Prioritas"
            min="1"
          />
        </li>
      </ul>
      <button @click="submitSelections">Lihat Rekomendasi</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      budget: null, // Jumlah uang pengguna
      items: [], // Daftar barang dari backend
      selectedItems: [], // Barang yang dipilih oleh pengguna
    };
  },
  created() {
    this.fetchItems();
  },
  methods: {
    fetchItems() {
      // Ambil daftar barang dari backend
      fetch("/items/")
        .then((response) => response.json())
        .then((data) => {
          this.items = data.map((item) => ({
            ...item,
            priority: 1, // Tambahkan properti priority default
          }));
        })
        .catch((error) => console.error("Error fetching items:", error));
    },
    submitBudget() {
      if (!this.budget || this.budget <= 0) {
        alert("Jumlah uang harus lebih besar dari 0.");
        return;
      }
      alert(`Jumlah uang: Rp ${this.budget}`);
    },
    submitSelections() {
      if (!this.budget || this.budget <= 0) {
        alert("Masukkan jumlah uang yang valid.");
        return;
      }

      const payload = {
        budget: this.budget,
        items: this.selectedItems.map((item) => ({
          id: item.id,
          priority: item.priority,
        })),
      };

      fetch("/items/recommendation/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      })
        .then((response) => {
          if (!response.ok) {
            console.error(`HTTP error! Status: ${response.status}`);
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then(() => {
          this.$router.push({
            name: "Recommendation",
            query: { budget: this.budget },
          });
        })
        .catch((error) => console.error("Error submitting selections:", error));
    },
  },
};
</script>

<style>
/* Tambahkan gaya opsional di sini */
form {
  margin-bottom: 2rem;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  margin-bottom: 1rem;
}
button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background-color: #45a049;
}
</style>

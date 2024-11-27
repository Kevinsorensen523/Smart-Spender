<template>
  <div>
    <h1>Rekomendasi Barang</h1>
    <p>Uang Anda: Rp {{ budget }}</p>
    <h2>Daftar Rekomendasi</h2>
    <ul>
      <li v-for="item in recommendedItems" :key="item.id">
        {{ item.name }} - Rp {{ item.price }} (Jumlah: {{ item.quantity }})
      </li>
    </ul>
    <p v-if="remainingBudget">Sisa Budget: Rp {{ remainingBudget }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      budget: null,
      recommendedItems: [],
      remainingBudget: 0,
    };
  },
  created() {
    // Ambil data budget dan selectedItems dari localStorage
    const selectedItems =
      JSON.parse(localStorage.getItem("selectedItems")) || [];
    const budget = localStorage.getItem("budget");

    if (!budget || selectedItems.length === 0) {
      alert("Data tidak lengkap. Kembali ke halaman sebelumnya.");
      this.$router.push("/budget");
    } else {
      this.budget = budget;
      this.fetchRecommendations(selectedItems);
    }
  },
  methods: {
    fetchRecommendations(selectedItems) {
      const requestData = {
        budget: this.budget,
        items: selectedItems,
      };

      fetch("/items/recommendation/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      })
        .then((res) => res.json())
        .then((data) => {
          console.log("Data Rekomendasi dari Backend:", data);
          if (data.recommendations && data.recommendations.length > 0) {
            this.recommendedItems = data.recommendations;
            this.remainingBudget = data.remaining_budget;
          } else {
            alert(data.message || "Tidak ada rekomendasi yang tersedia.");
          }
        })
        .catch((err) => {
          console.error("Error fetching recommendations:", err);
          alert("Terjadi kesalahan saat mengambil rekomendasi.");
        });
    },
  },
};
</script>

<style>
/* Tambahkan gaya opsional di sini */
</style>

<template>
  <div>
    <h1>Daftar Barang</h1>
    <ul>
      <li v-for="item in items" :key="item.id">
        {{ item.name }} - Rp {{ item.price }}
        <button @click="editItem(item)">Edit</button>
        <button @click="deleteItem(item.id)">Hapus</button>
      </li>
    </ul>

    <h2>Import CSV</h2>
    <form @submit.prevent="importCSV">
      <input type="file" ref="file" accept=".csv" />
      <button type="submit">Unggah CSV</button>
    </form>

    <h2>{{ isEditing ? "Edit Barang" : "Tambah Barang" }}</h2>
    <form @submit.prevent="saveItem">
      <input v-model="form.name" placeholder="Nama Barang" required />
      <input
        v-model.number="form.price"
        placeholder="Harga Barang"
        type="number"
        required
      />
      <button type="submit">
        {{ isEditing ? "Simpan Perubahan" : "Tambah" }}
      </button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      items: [],
      form: { id: null, name: "", price: "" },
      isEditing: false,
    };
  },
  created() {
    this.fetchItems();
  },
  methods: {
    fetchItems() {
      fetch("/items/")
        .then((res) => res.json())
        .then((data) => {
          this.items = data;
        });
    },
    saveItem() {
      if (this.isEditing) {
        // Edit Item
        fetch(`/items/${this.form.id}/`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.form),
        })
          .then((res) => res.json())
          .then(() => {
            this.fetchItems();
            this.resetForm();
          });
      } else {
        // Add New Item
        fetch("/items/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.form),
        })
          .then((res) => res.json())
          .then(() => {
            this.fetchItems();
            this.resetForm();
          });
      }
    },
    importCSV() {
      const file = this.$refs.file.files[0];
      if (!file) {
        alert("Pilih file CSV terlebih dahulu!");
        return;
      }

      const formData = new FormData();
      formData.append("file", file);

      fetch("/items/import_csv/", {
        method: "POST",
        body: formData,
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.error) {
            alert(`Error: ${data.error}`);
          } else {
            alert(data.message);
            this.fetchItems(); // Refresh data
          }
        })
        .catch((error) => {
          console.error("Error importing CSV:", error);
        });
    },
    editItem(item) {
      this.form = { ...item };
      this.isEditing = true;
    },
    deleteItem(id) {
      fetch(`/items/${id}/`, { method: "DELETE" }).then(() => {
        this.fetchItems();
      });
    },
    resetForm() {
      this.form = { id: null, name: "", price: "" };
      this.isEditing = false;
    },
  },
};
</script>

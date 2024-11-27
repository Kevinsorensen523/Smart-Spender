<template>
  <div id="app">
    <header>
      <h1>Smart Spender</h1>
    </header>

    <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/list-items">List Items</router-link>
      <router-link to="/budget">Start</router-link>
    </nav>

    <main>
      <router-view />
      <!-- Router view di sini -->
    </main>

    <footer>
      <p>&copy; 2024 Smart Spender</p>
    </footer>
  </div>
</template>

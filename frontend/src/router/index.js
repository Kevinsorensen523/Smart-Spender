import BudgetPage from "@/views/BudgetPage.vue";
import ListItemsPage from "@/views/ListItemsPage.vue";
import RecommendationPage from "@/views/RecommendationPage.vue";
import WelcomePage from "@/views/WelcomePage.vue";
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  { path: "/", name: "Welcome", component: WelcomePage },
  { path: "/list-items", name: "ListItems", component: ListItemsPage },
  { path: "/budget", name: "Budget", component: BudgetPage },
  {
    path: "/recommendation",
    name: "Recommendation",
    component: RecommendationPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

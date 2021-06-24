<template>
  <div id="wrapper">
    <the-header></the-header>
    <section class="section p-0">
      <router-view></router-view>
    </section>
    <footer class="footer mt-5">
      <p class="has-text-centered is-size-4">OO CLINIC</p>
      <p class="has-text-centered is-size-7">
        <i class="fas fa-phone"> </i> 000 . 0000. 0000
      </p>
      <br />
      <p class="has-text-centered">copyright (c) 2021</p>
    </footer>
  </div>
</template>

<script>
import axios from "axios";
import TheHeader from "./components/layout/TheHeader.vue";

export default {
  name: "App",
  components: {
    TheHeader,
  },
  beforeCreate() {
    this.$store.dispatch("initializeStore");
    const token = this.$store.state.token;
    if (token) {
      axios.defaults.headers.common["Authorization"] = "token " + token;
    } else {
      axios.defaults.headers.common["Authorization"] = "";
    }
  },
};
</script>

<style lang="scss">
@import "../node_modules/bulma";
@import "../node_modules/bulma-timeline";
@import "../node_modules/bulma-pageloader";
@import "../node_modules/@creativebulma/bulma-tooltip";
</style>

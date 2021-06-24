import { createStore } from "vuex";

export default createStore({
  state: {
    user: {
      username: "",
      userType: "", // is doctor? is manager? is patient?
      email: "",
    },
    isAuthenticated: false,
    token: "",
  },
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem("token")) {
        state.token = localStorage.getItem("token");
        state.isAuthenticated = true;
        state.user.userType = localStorage.getItem("userType");
        state.user.email = localStorage.getItem("email");
      } else {
        state.isAuthenticated = false;
        state.token = "";
        state.user.userType = "";
        state.user.email = "";
      }
    },
    setToken(state, token) {
      state.token = token;
      state.isAuthenticated = true;
    },
    removeToken(state) {
      state.token = "";
      state.isAuthenticated = false;
      state.user.userType = "";
      state.user.email = "";
    },
  },
  actions: {
    initializeStore(context) {
      context.commit('initializeStore')
    },
    setToken(context, payload) {
      context.commit("setToken", payload);
    },
    removeToken(context) {
      context.commit("removeToken");
    },
  },
  modules: {},
});

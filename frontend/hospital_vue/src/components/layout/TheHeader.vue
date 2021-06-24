<template>
  <div class="page-navbar">
    <nav class="navbar is-info is-fixed-top">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item is-size-4"><strong>Hospital Appintment</strong></router-link>
      </div>
      <div class="navbar-menu">
        <div class="navbar-end">
          <router-link to="/doctors" class="navbar-item"><strong>Doctors</strong></router-link>
          <router-link class="navbar-item" to="/appointment"><strong>Make an Appointment</strong></router-link>

          <!-- manager menu -->
          <template v-if="$store.state.isAuthenticated && $store.state.user.userType === 'manager'">
            <router-link class="navbar-item" to="/appointment/user"><strong>Appointments</strong></router-link>
            <router-link class="navbar-item" to="/user-control"><strong>Users</strong></router-link>
            <div class="navbar-item">
              <button class="button is-danger" @click="logout">Log out</button>
            </div>
          </template>

          <!-- doctor menu -->
          <template v-else-if="$store.state.isAuthenticated && $store.state.user.userType === 'doctor'">
            <router-link class="navbar-item" to="/appointment/user"><strong>Appointments</strong></router-link>
            <div class="navbar-item has-dropdown is-hoverable">
              <div class="navbar-link">Account</div>
              <div class="navbar-dropdown is-right">
                <router-link class="navbar-item"
                  :to="{ name: 'DoctorInfo', params: { email: $store.state.user.email },}">
                  Doctor Info
                </router-link>
              </div>
            </div>
            <div class="navbar-item">
              <button class="button is-danger" @click="logout">Log out</button>
            </div>
          </template>

          <!-- patient manu -->
          <template v-else-if=" $store.state.isAuthenticated && $store.state.user.userType === 'patient'">
            <div class="navbar-item has-dropdown is-hoverable">
              <div class="navbar-link">Account</div>
              <div class="navbar-dropdown is-right">
                <router-link class="navbar-item"
                  :to="{ name: 'PatientInfo', params: { email: $store.state.user.email },}">
                  Patient Info
                </router-link>
                <router-link class="navbar-item" to="/appointment/user">Appointments</router-link>
              </div>
            </div>
            <div class="navbar-item">
              <button class="button is-danger" @click="logout">Log out</button>
            </div>
          </template>

          <!-- unauthenticated menu -->
          <template v-else>
            <div class="navbar-item">
              <div class="buttons">
                <router-link to="/log-in" class="button is-primary">Log in</router-link>
                <router-link to="/sign-up" class="button is-success">Sign up</router-link>
              </div>
            </div>
          </template>
          
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "TheHeader",
  methods: {
    logout() {
      axios
        .post("/api/token/logout/")
        .then((res) => {
          axios.defaults.headers.common["Authorization"] = "";
          localStorage.removeItem("token");
          localStorage.removeItem("userType");
          localStorage.removeItem("email");
          this.$store.dispatch("removeToken");

          this.$router.push("/");
        })
        .catch((err) => {
          if (err.response) {
            console.log(JSON.stringify(err.response.data));
          } else if (err.message) {
            console.log(JSON.stringify(err.message));
          } else {
            console.log(JSON.stringify(err));
          }
        });
    },
  },
};
</script>

<style scoped></style>

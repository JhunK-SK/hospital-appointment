<template>
  <div class="page-user-control">
    <div
      class="pageloader is-bottom-to-top is-info"
      :class="isLoading ? 'is-active' : ''">
      <span class="title">Loading...</span>
    </div>
    <div class="columns is-multiline">
      <div class="column is-12">
        <section class="hero is-info is-small">
          <div class="hero-body">
            <h1 class="title is-size-5 has-text-white">User control</h1>
          </div>
        </section>
      </div>
      <div class="column is-3 ml-4">
        <div class="field has-addons">
          <div class="control has-icons-left  is-expanded">
            <input
              class="input is-small"
              type="text"
              placeholder="Search"
              v-model="keyword"/>
            <span class="icon is-small is-left">
              <i class="fas fa-search"></i>
            </span>
          </div>
          <div class="control">
            <button class="button is-info is-small" @click="searchData">
              Go
            </button>
          </div>
        </div>
      </div>
      <div class="column is-12">
        <div class="box">
          <table class="table is-fullwidth is-hoverable is-size-7">
            <thead>
              <tr>
                <th style="width: 400px;">Eamil</th>
                <th>Name</th>
                <th>
                  <div class="select is-small">
                    <select v-model="selectedType" @change="sortUserListByType">
                      <option value="all" selected>All type</option>
                      <option value="doctor">Doctor</option>
                      <option value="manager">Manager</option>
                      <option value="patient">Patient</option>
                    </select>
                  </div>
                </th>
                <th>Joined date</th>
                <th></th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="user in filteredUsers" :key="user.id">
                <td>{{ user.email }}</td>
                <td>{{ user.get_full_name }}</td>
                <td>{{ user.user_type }}</td>
                <td>{{ user.get_joined_data_formatted }}</td>
                <td v-if="user.user_type === 'doctor'">
                  <router-link
                    :to="{ name: 'DoctorInfo', params: { email: user.email } }">
                    Details
                    </router-link>
                </td>
                <td v-else>
                  <router-link
                    :to="{ name: 'PatientInfo', params: { email: user.email } }">
                    Details
                  </router-link>
                </td>
                
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "UserControl",
  data() {
    return {
      isLoading: false,
      users: [],
      filteredUsers: [],
      keyword: "",
      selectedType: "all",
    };
  },
  beforeCreate() {
    if (
      this.$store.state.user.userType === "patient" ||
      this.$store.state.user.userType === "doctor"
    ) {
      this.$router.push("/");
    }
  },
  async mounted() {
    await this.getUsers();
  },
  computed: {
    sortUserListByType() {
      if (this.selectedType !== "all") {
        this.filteredUsers = this.users.filter(
          (user) => user.user_type === this.selectedType
        );
      } else {
        this.filteredUsers = this.users;
      }
    },
  },
  methods: {
    getUsers() {
      this.isLoading = true;
      axios.get("/api/accounts/").then((res) => {
        console.log('users: ', res.data)
        this.users = res.data;
        this.filteredUsers = this.users;
        this.isLoading = false;
      });
    },
    searchData() {
      axios
        .get(
          `/api/accounts/?q=${this.keyword}`)
        .then((res) => {

          this.users = res.data;
          this.filteredUsers = this.users;
        });
    },
  },
};
</script>

<style scoped></style>

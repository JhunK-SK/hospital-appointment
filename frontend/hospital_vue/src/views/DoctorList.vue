<template>
  <div class="page-doctor-list">
    <div class="pageloader is-bottom-to-top is-info" :class="isLoading ? 'is-active': ''">
      <span class="title">Loading...</span>
    </div>
    <div class="columns is-multiline">
      <div class="column is-12">
        <section class="hero is-info is-small">
          <div class="hero-body">
            <h1 class="title is-size-5 has-text-white">Our Doctors</h1>
          </div>
        </section>
      </div>
      <div class="column is-10 is-offset-1">
        <div class="columns is-multiline">
          <div class="column is-3" v-for="doctor in doctors" :key="doctor.id">
            <div class="card">
              <div class="card-image">
                <figure class="image is-fullwidth is-4by3">
                  <img :src="doctor.picture" alt="" />
                </figure>
              </div>
              <div class="card-content">
                <p class="title is-size-5">{{ doctor.user.get_full_name }}</p>
                <p class="is-size-6">specialty: {{ doctor.specialty }}</p>
                <p class="is-size-6">Email: {{ doctor.user.email }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "DoctorList",
  data() {
    return {
      isLoading: false,
      doctors: [],
    };
  },
  mounted() {
    this.getDoctors();
  },
  methods: {
    getDoctors() {
      this.isLoading = true;
      axios.get("/api/doctor-list/").then((res) => {
        this.isLoading = false;
        this.doctors = res.data;
        console.log(this.doctors);
      }).catch(err => {
        console.log(JSON.stringify(err))
      });
    },
  },
};
</script>

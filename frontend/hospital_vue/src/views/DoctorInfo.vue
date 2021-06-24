<template>
  <div class="page-doctor-info">
    <div class="columns is-multiline">
      <div class="column is-12 mt-4 ml-4">
        <h1 class="title">Doctor Information</h1>
        <p class="subtitle is-size-6">
          specialiezed in
        </p>
      </div>
      <div class="column is-6 is-offset-3">
        <form @submit.prevent="submitForm">
          <div class="field" v-if="$store.state.user.userType === 'manager'">
            <div class="control">
              <div class="select">
                <select v-model="doctor.user.user_type">
                  <option value="doctor">Doctor</option>
                  <option value="patient">Patient</option>
                  <option value="manager">Manager</option>
                </select>
              </div>
            </div>
          </div>
          <div class="field">
            <label for="">Email</label>
            <div class="control">
              <input
                type="email"
                class="input"
                v-model="doctor.user.email"
                disabled
              />
            </div>
          </div>
          <label for="">Profile picture</label>
          <div class="control">
            <input type="text" class="input" disabled v-model="doctor.picture">
          </div>
          <div class="field has-addons">
            <input
              type="file"
              class="input is-small"
              @change="selectImageFile"/>
            <div class="control">
              <button
                class="button is-link is-small"
                @click.prevent="uploadImageFile">
                Set
              </button>
            </div>
          </div>
          <div class="field">
            <label for="">First Name</label>
            <div class="control">
              <input
                type="text"
                class="input"
                v-model.trim="doctor.first_name"/>
            </div>
          </div>
          <div class="field">
            <label for="">Last Name</label>
            <div class="control">
              <input
                type="text"
                class="input"
                v-model.trim="doctor.last_name"/>
            </div>
          </div>
          <div class="field">
            <label for="">Medical Specialty</label>
            <div class="control">
              <input
                type="text"
                class="input"
                v-model.trim="doctor.specialty"/>
            </div>
          </div>
          <button class="button is-success">Update details</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "DoctorInfo",
  props: ["email"],
  data() {
    return {
      selectedFile: null,
      doctor: {
        user: {},
      },
    };
  },
  async mounted() {
    await this.getOrCreateDoctorDetails();
  },
  methods: {
    getOrCreateDoctorDetails() {
      axios
        .get(`/api/doctors/?email=${this.email}`)
        .then((res) => {
          this.doctor = res.data[0];
        });
    },
    submitForm() {
      axios
        .patch(`/api/doctors/${this.doctor.id}/?email=${this.email}`, this.doctor)
        .then((res) => {
          if (this.doctor.user.user_type === "patient") {
            this.$router.push({
              name: "PatientInfo",
              params: { email: this.doctor.user.email },
            });
          }
        })
        .catch((err) => {
          console.log(JSON.stringify(err));
        });
    },
    selectImageFile(event) {
      this.selectedFile = event.target.files[0];
    },
    uploadImageFile() {
      let formData = new FormData();
      formData.append("file", this.selectedFile);
      axios
        .patch(`/api/doctor-picture/${this.doctor.id}/`, formData, {
          headers: { "Content-Type": "multipart/form-data", }, })
        .then((res) => {
          this.doctor.picture = this.selectedFile.name
        })
        .catch(err => {
          console.log(JSON.stringify(err))
        })
    },
  },
};
</script>

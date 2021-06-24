<template>
  <div class="page-user-appointments">
    <div
      class="pageloader is-bottom-to-top is-info"
      :class="isLoading ? 'is-active' : ''">
      <span class="title">Loading...</span>
    </div>
    <div class="columns is-multiline">
      <div class="column is-12">
        <section class="hero is-info is-small">
          <div class="hero-body">
            <h1 class="title is-size-5 has-text-white">
              {{ whoseAppointments }}
            </h1>
            <p
              class="subtitle is-size-6"
              v-if="$store.state.user.userType === 'patient'">
              To cancel the appointment, please contact our office.
            </p>
          </div>
        </section>
      </div>

      <div class="column is-3 ml-4" v-if="$store.state.user.userType === 'manager'">
        <div class="field has-addons">
          <div class="control has-icons-left  is-expanded">
            <input
              class="input is-small"
              type="text"
              placeholder="Doctor name or patient name..."
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

      <!-- date-search -->
      <div class="column is-3" v-if="$store.state.user.userType === 'manager'">
        <div class="field has-addons">
          <div class="control">
            <v-date-picker
              v-model="selectedDate"
              :input-debounce="500"
              :model-config="modelConfig"
              :disabled-dates="disabledDates"
              :first-day-of-week="1">
              <template v-slot="{ inputValue, inputEvents }">
                <input
                  class="input is-small"
                  v-on="inputEvents"
                  :value="inputValue"/>
              </template>
            </v-date-picker>
          </div>
          <div class="control">
            <button class="button is-info is-small" @click="searchData">
              Date Search
            </button>
          </div>
          <div class="control">
            <button class="button is-success is-small" @click="dateReset">
              Date Reset
            </button>
          </div>
        </div>
      </div>
      <!-- date-search end -->
      <div class="column is-12">
        <div class="box">
          <!-- pagination -->
          <nav
            class="pagination is-small is-right"
            role="navigation"
            aria-label="pagination">
            <button
              class="pagination-previous button is-small is-info is-outlined"
              :disabled="!hasPrevious"
              @click="gotoPage(currentPage - 1)">
              Previous
            </button>
            <button
              class="pagination-previous button is-small is-info is-outlined"
              :disabled="!hasNext"
              @click="gotoPage(currentPage + 1)">
              Next
            </button>
            <ul class="pagination-list"></ul>
          </nav>
          <!-- pagination end -->

          <table class="table is-fullwidth is-size-7">
            <thead>
              <tr>
                <th style="width: 180px;">Doctor</th>
                <th style="width: 180px;">Department</th>
                <th style="width: 180px;">Time</th>
                <th
                  v-if="$store.state.user.userType === 'manager'"
                  style="width: 180px;">
                  Patient
                </th>
                <th>Symptoms</th>
                <th v-if="$store.state.user.userType === 'manager'">Edit</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="appointment in appointments" :key="appointment.id">
                <td>{{ appointment.doctor.user.get_full_name }}</td>
                <td>{{ appointment.doctor.specialty }}</td>
                <td>{{ appointment.date }} - {{ appointment.timeslot }}</td>
                <td v-if="$store.state.user.userType === 'manager'">
                  <router-link
                    :to="{ name: 'PatientInfo', params: { email: appointment.patient.user.email },}">
                    {{ appointment.patient.user.get_full_name }}
                  </router-link>
                </td>
                <td>
                  <a
                    class="has-tooltip-right has-tooltip-arrow has-tooltip-info has-tooltip-multiline"
                    :data-tooltip="appointment.symptom"
                    >see symptom</a>
                </td>
                <td v-if="$store.state.user.userType === 'manager'">
                  <div class="buttons">
                    <button class="button is-small is-warning">
                      <router-link
                        :to="{ name: 'EditAppointment', params: { id: appointment.id },}">
                        Edit
                      </router-link>
                    </button>
                    <button
                      class="button is-small is-danger"
                      @click="cancelAppointment(appointment.id)">
                      Cancel
                    </button>
                  </div>
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
  name: "UserAppointments",
  data() {
    return {
      keyword: "",
      selectedDate: "",
      currentPage: Number(this.$route.query.pageNumber) || 1,
      totalPage: 1,
      hasPrevious: false,
      hasNext: false,
      isLoading: false,
      appointments: [],
      timeslots: [
          "09:00", "09:15", "09:30", "09:45",
          "10:00", "10:15", "10:30", "10:45",
          "11:00", "11:15", "11:30", "11:45",
          "12:00", "12:15", "12:30", "12:45", 
          "14:00", "14:15", "14:30", "14:45",
          "15:00", "15:15", "15:30", "15:45",
          "16:00", "16:15", "16:30", "16:45",
          "17:00", "17:15", "17:30", "17:45",
      ],
      modelConfig: {
        type: "string",
        mask: "YYYY-MM-DD", // Uses 'iso' if missing
      },
      disabledDates: [{ weekdays: [1, 7] }],
    };
  },
  mounted() {
    this.getAppointments();
  },
  computed: {
    whoseAppointments() {
      if (this.$store.state.user.userType === "patient") {
        return "My appointments";
      } else {
        return "Appointments";
      }
    },
  },
  methods: {
    dateReset() {
      this.selectedDate = "";
    },
    gotoPage(selectedPage) {
      this.currentPage = selectedPage;
      this.getAppointments();
    },
    getAppointments() {
      this.isLoading = true;
      this.$router.push({
        path: this.$route.path,
        query: { pageNumber: this.currentPage },
      });

      axios
        .get(`/api/appointments/?page=${this.currentPage}`)
        .then((res) => {
          console.log(res);

          this.isLoading = false;
          this.appointments = res.data.results;
          for (const appointment of this.appointments) {
            appointment.timeslot = this.timeslots[appointment.timeslot];
          }

          if (res.data.previous) {
            this.hasPrevious = true;
          } else {
            this.hasPrevious = false;
          }
          if (res.data.next) {
            this.hasNext = true;
          } else {
            this.hasNext = false;
          }
          this.totalPage = res.data.total_page;
        })
        .catch((err) => {
          console.log(JSON.stringify(err));
        });
    },
    async cancelAppointment(appointmentId) {
      await axios
        .delete(`/api/appointments/${appointmentId}/`)
        .then((res) => {})
        .catch((err) => {
          console.log(JSON.stringify(err));
        });

      if (this.keyword) {
        this.searchData();
      } else {
        this.getAppointments();
      }
    },
    searchData() {
      axios
        .get(`/api/appointments/?q=${this.keyword}&date=${this.selectedDate}`)
        .then((res) => {
          console.log(res);
          this.appointments = res.data.results;
          for (const appointment of this.appointments) {
            appointment.timeslot = this.timeslots[appointment.timeslot];
          }

          if (res.data.previous) {
            this.hasPrevious = true;
          } else {
            this.hasPrevious = false;
          }
          if (res.data.next) {
            this.hasNext = true;
          } else {
            this.hasNext = false;
          }
          this.totalPage = res.data.total_page;
        })
        .catch((err) => {
          console.log(JSON.stringify(err));
        });
    },
  },
};
</script>

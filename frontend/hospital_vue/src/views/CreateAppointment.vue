<template>
  <div class="page-create-appointment">
    <div class="pageloader is-bottom-to-top is-info" :class="isLoading ? 'is-active': ''">
      <span class="title">Loading...</span>
    </div>
    <div class="columns is-multiline">
      <div class="column is-12">
        <section class="hero is-info is-small">
          <div class="hero-body">
            <h1 class="title is-size-5 has-text-white">Make an appointment</h1>
          </div>
        </section>
      </div>
      <div class="column is-6 is-offset-3">
        <form @submit.prevent="submitForm">
          <div class="field">
            <label for=""><strong>Doctor</strong></label>
            <div class="control is-expanded">
                <div class="select is-primary">
                    <select v-model="appointment.doctor" @change="getUnAvailableTimeSlots">
                        <option value="">Select Doctor</option>
                        <option
                            :value="doctor.id"
                            v-for="doctor in doctors"
                            :key="doctor.id">
                            {{ doctor.user.get_full_name }} - {{ doctor.specialty }}
                        </option>
                    </select>
                </div>
            </div>

            <!-- if request.user is patient -->
            <div class="field mt-3" v-if="$store.state.user.userType === 'patient'">
              <label for=""><strong>Patient</strong></label>
              <div class="control">
                <input
                  v-if="patient.user"
                  type="text"
                  class="input"
                  :value="patient.user.get_full_name"
                  disabled/>
              </div>
            </div>  <!-- if request.user is patient ends -->

            <!-- if request.user is manager or doctor -->
            <div v-else class="columns is-multiline">
              <div class="column is-2 mt-3">
                <label for=""><strong>Patient</strong></label>
              </div>
              <div class="column is-10 mt-3" v-if="patient.user">
                <span class="tag is-primary">{{ patient.user.get_full_name }} - {{ patient.user.email }}</span>
              </div>
              <div class="column is-12 pt-0 pb-0">
                <div class="field has-addons">
                    <div class="control has-icons-left  is-expanded">
                        <input class="input is-small" type="text" placeholder="Search patient(email or name)" v-model="keyword">
                        <span class="icon is-small is-left">
                            <i class="fas fa-search"></i>
                        </span>
                    </div>
                    <div class="control">
                        <button class="button is-info is-small" @click.prevent="searchData">Go</button>
                    </div>
                </div>
              </div>
            </div>
            <div class="columns is-multiline is-size-7 pb-0 is-vcentered" v-for="patient in filteredPatients" :key="patient.id">
              <div class="column is-3">
                <p>{{ patient.user.get_full_name }}</p>
              </div>
              <div class="column is-3">
                {{ patient.user.email }}
              </div>
              <div class="column is-4">
                {{ patient.insurance_number }}
              </div>
              <div class="column is-2">
                <button class="is-focused button is-small" @click.prevent="selectPatient(patient.id)">Select</button>
              </div>
            </div>  <!-- if request.user is manager or doctor ends -->

            <!-- Date & Timeslots -->
            <div class="columns">
              <div class="column is-5">
                <div class="field">
                  <label for=""><strong>Date</strong></label>
                  <div class="control">
                    <v-date-picker
                      color="teal"
                      v-model="appointment.date"
                      :first-day-of-week="1"
                      :model-config="modelConfig"
                      :disabled-dates="disabledDates"
                      @dayclick="getUnAvailableTimeSlots"
                    ></v-date-picker>
                  </div>
                </div>
              </div>
              <div class="column is-7">
                <div class="columns is-multiline is-centered">
                  <div class="column is-12">
                    <div class="field">
                      <label for=""><strong>Time</strong></label>
                    </div>
                  </div>
                  <div class="column is-12 has-text-centered p-0">
                    <button
                      class="button is-small is-link is-inverted mr-2"
                      @click.prevent="selectTab('morning')">
                      Morning
                    </button>
                    <button
                      class="button is-small is-success is-inverted mr-2"
                      @click.prevent="selectTab('afternoon')">
                      Afternoon
                    </button>
                  </div>
                  <div
                    class="columns is-multiline m-0"
                    v-if="selectedTab === 'morning'">
                    <div
                      class="column is-3"
                      v-for="(timeslot, index) in timeslots.slice(0, 16)"
                      :key="timeslot">
                      <p
                        class="button is-small is-rounded is-light is-link is-hoverable is-active"
                        value="timeslot"
                        @click.prevent="getTimeSlot(timeslot, index)"
                        :disabled="checkIfBooked(index)">
                        {{ timeslot }}
                      </p>
                    </div>
                  </div>
                  <div class="columns is-multiline m-0" v-if="selectedTab === 'afternoon'">
                    <div
                      class="column is-3"
                      v-for="(timeslot, index) in timeslots.slice(16, 32)"
                      :key="timeslot">
                      <p
                        class="button is-small is-rounded is-light is-success is-hoverable is-active"
                        value="timeslot"
                        @click="getTimeSlot(timeslot, index + 16)"
                        :disabled="checkIfBooked(index + 16)">
                        {{ timeslot }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>  <!-- Date & Timeslots ends -->

            <!-- display selected date and timeslot -->
            <div class="field" v-if="appointment.date">
              <div class="content is-size-5">{{ appointment.date }} - {{ timeslots[timeslotIndex] }}</div>
            </div> <!-- display selected date and timeslot ends -->


            <div class="field">
                <label for=""><strong>Symptom</strong></label>
                <div class="control">
                    <textarea v-model="appointment.symptom" rows="3" class="textarea is-primary" placeholder="Please describe your symptom or purpose of visit briefly.."></textarea>
                </div>
            </div>

            <div class="control">
                <button class="button is-primary is-fullwidth">Make an appointment</button>
            </div>

          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "CreateAppointment",
  async beforeCreate() {
    let email;
    let isFilledUserInfo;
    await axios
      .get("/api/users/me")
      .then((res) => {
        email = res.data["email"];
      })
      .catch((err) => {
        console.log(JSON.stringify(err));
      });

    await axios.get(`/api/patients/?email=${email}`).then((res) => {
      isFilledUserInfo = res.data[0].is_filled_in;
    });

    // check if request user(patient) has filled out the detail form(insurance number).
    if (isFilledUserInfo === false) {
      this.$router.push({ name: "PatientInfo", params: { email: email } });
    }
  },
  data() {
    return {
      isLoading: false,
      keyword: '',
      filteredPatients: [],
      patient: {},
      doctors: [],
      appointment: {
        doctor: "",
      },
      disabledDates: [
        { weekdays: [1, 7] },
        { start: null, end: new Date() },
      ],
      selectedTab: "morning",
      timeslotIndex: '',
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
      unavailableTimeSlots: [],
      modelConfig: {
        type: "string",
        mask: "YYYY-MM-DD", // Uses 'iso' if missing
      },
    };
  },
  mounted() {
    this.getDoctors();
    this.getPatientInfo();
  },
  methods: {
    getDoctors() {
      // for doctor selections.
      this.isLoading = true
      axios.get("/api/doctor-list/").then((res) => {
        this.isLoading = false
        this.doctors = res.data;
      });
    },
    getPatientInfo() {
      const userType = localStorage.getItem("userType");
      const email = localStorage.getItem("email");

      if (userType === "patient") {
        axios
          .get(`/api/patients/?email=${email}`)
          .then((res) => {
          this.patient = res.data[0];
          })
          .catch(err => {
            console.log(JSON.stringify(err))
          });
      }
    },
    selectTab(tab) {
      // for time slots either morning or afternoon.
      this.selectedTab = tab;
    },
    getTimeSlot(timeslot, index) {
        if(!this.checkIfBooked(index)) {
          this.timeslotIndex = this.timeslots.indexOf(timeslot)
        }
    },
    checkIfBooked(index) {
      if(this.unavailableTimeSlots.includes(index)) {
        return true
      } else {
        false
      }
    },
    submitForm() {
        const dataForm = {
            doctor : this.appointment.doctor,
            patient : this.patient.id,
            date : this.appointment.date,
            timeslot : this.timeslotIndex,
            symptom : this.appointment.symptom
        }
        console.log(dataForm)
        axios.post('/api/appointments/', dataForm)
        .then(res => {
          this.$router.push({name: 'UserAppointments'})
        })
        .catch(err => {
          console.log(JSON.stringify(err))
        })
    },
    searchData() {
      const searchType = 'patient'
      axios.get(`/api/patients/?searchtype=${searchType}&q=${this.keyword}`)
      .then(res => {
        this.filteredPatients = res.data.filter(patient => patient.user.user_type === 'patient')
      })
    },
    selectPatient(patientId) {
      const patient = this.filteredPatients.filter(patient => patient.id === patientId)[0]
      this.patient = patient
    },
    getUnAvailableTimeSlots() {
      this.unavailableTimeSlots = []
      if(this.appointment.doctor && this.appointment.date) {
        const doctor_id = this.appointment.doctor
        const date = this.appointment.date

        axios.get(`/api/appointment-timeslots/?doctor=${doctor_id}&date=${date}`)
        .then(res => {
        
          for (const appointment of res.data) {
            this.unavailableTimeSlots.push(appointment.timeslot)
          }

        })
      }
    },
  },
};
</script>

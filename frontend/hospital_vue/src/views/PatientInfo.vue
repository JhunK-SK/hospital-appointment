<template>
  <div class="page-patient-info">
    <div class="columns is-multiline">
      <div class="column is-12 mt-4 ml-4">
        <h1 class="title">Patient Information</h1>
        <p class="subtitle is-size-6">
          To make an appointment, user details should be filled in
        </p>
      </div>
      <div class="column is-6 is-offset-3">
        <form @submit.prevent="submitForm">
          <div class="field" v-if="$store.state.user.userType === 'manager'">
            <div class="control">
              <div class="select">
                <select v-model="patient.user.user_type">
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
                v-model="patient.user.email"
                disabled/>
            </div>
          </div>
          <div class="field">
            <label for="">First Name</label>
            <div class="control">
              <input type="text" class="input" v-model.trim="patient.first_name" />
            </div>
          </div>
          <div class="field">
            <label for="">Last Name</label>
            <div class="control">
              <input type="text" class="input" v-model.trim="patient.last_name" />
            </div>
          </div>
          <div class="field">
            <label for="">Insurance No.</label>
            <div class="control">
              <input
                type="text"
                class="input"
                v-model="patient.insurance_number"/>
              <p v-if="insuranceNumberValidity === 'invalid'" class="has-text-danger">
                To update patient information, this insurance number has to be filled in.
              </p>
            </div>
          </div>
          <div class="field">
            <label for="">Gender</label>
            <div class="control">
              <div class="select">
                <select name="" id="" v-model="patient.gender">
                  <option value="male" selected>Male</option>
                  <option value="female">Female</option>
                </select>
              </div>
            </div>
          </div>
          <div class="field">
            <label for="">Date of birth</label>
            <div class="control">
              <v-date-picker :model-config="modelConfig" v-model="patient.date_of_birth">
                <template v-slot="{ inputValue, inputEvents }">
                  <input
                    class="input"
                    :value="inputValue"
                    v-on="inputEvents"/>
                </template>
              </v-date-picker>
            </div>
          </div>
          <div class="field">
            <label for="">Height(cm)</label>
            <div class="control">
              <input type="number" class="input" v-model="patient.height" />
            </div>
          </div>
          <div class="field">
            <label for="">Weight(kg)</label>
            <div class="control">
              <input type="number" class="input" v-model="patient.weight" />
            </div>
          </div>
          <div class="field">
            <label for="">Address 1</label>
            <div class="control">
              <input type="text" class="input" v-model="patient.address1" />
            </div>
          </div>
          <div class="field">
            <label for="">Address 2</label>
            <div class="control">
              <input type="text" class="input" v-model="patient.address2" />
            </div>
          </div>
          <div class="field">
            <label for="">City</label>
            <div class="control">
              <input type="text" class="input" v-model="patient.city" />
            </div>
          </div>
          <div class="field">
            <label for="">State</label>
            <div class="control">
              <input type="text" class="input" v-model="patient.state" />
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
  name: "PatientInfo",
  props: ["email"],
  data() {
    return {
      patient: {
        user: {}
      },
      modelConfig: {
        type: 'string',
        mask: 'YYYY-MM-DD',
      },
      insuranceNumberValidity: '',
    };
  },
  async mounted() {
    await this.getOrCreatePatientDetails();
  },
  methods: {
    getOrCreatePatientDetails() {
      axios.get(`/api/patients/?email=${this.email}`).then((res) => {
        this.patient = res.data[0];
      });
    },
    submitForm() {
        console.log(this.patient)
        if(this.patient.insurance_number === '' || this.patient.insurance_number === null) {
            this.insuranceNumberValidity = 'invalid'
            this.patient.is_filled_in = false
            return
        }
        this.insuranceNumberValidity = 'valid'
        this.patient.is_filled_in = true
      axios
        .patch(`/api/patients/${this.patient.id}/?email=${this.email}`, this.patient)
        .then((res) => {
          if(this.patient.user.user_type === 'doctor') {
            this.$router.push({ name: 'DoctorInfo', params: { email: this.patient.user.email }})
          }
        })
        .catch((err) => {
          console.log(JSON.stringify(err));
        });
    },
  },
};
</script>

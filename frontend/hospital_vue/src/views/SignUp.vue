<template>
    <div class="page-signup">
        <div class="columns">
            <div class="column is-4 is-offset-4 mt-4">
                <h1 class="title mb-2">Sign up</h1>
                <form @submit.prevent="submitForm" class="form">
                    <div class="field">
                        <div class="control">
                            <input type="email" class="input" placeholder="Your email" v-model="email">
                        </div>
                    </div>
                    <div class="field">
                        <div class="control">
                            <input type="password" class="input" placeholder="Your password" v-model="password">
                        </div>
                    </div>
                    <div class="field">
                        <div class="control">
                            <input type="text" class="input" placeholder="First Name" v-model="firstName">
                        </div>
                    </div>
                    <div class="field">
                        <div class="control">
                            <input type="text" class="input" placeholder="Last Name" v-model="lastName">
                        </div>
                    </div>
                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" :key="error">{{ error }}</p>
                    </div>
                    <div class="control">
                        <button class="button is-fullwidth is-success">Sign up</button>
                    </div>
                </form>
                <hr>
                <router-link to="/log-in">Log in</router-link>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: 'SignUp',
    data() {
        return {
            email: '',
            password: '',
            firstName: '',
            lastName: '',
            errors: []
        }
    },
    methods: {
        submitForm() {
            const formData = {
                email: this.email,
                password: this.password,
                first_name: this.firstName,
                last_name: this.lastName,
            }
            axios
                .post('/api/users/', formData)
                .then(res => {
                    this.$router.push('/log-in')
                })
                .catch(err => {
                    if (err.message){
                        console.log(JSON.stringify(err.message))
                    } else {
                        console.log(JSON.stringify(err))
                    }
                })
        }
    },
}
</script>

<style scoped>

</style>
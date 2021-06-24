<template>
    <div class="page-login">
        <div class="columns">
            <div class="column is-4 is-offset-4 mt-4">
                <h1 class="title mb-2">Log in</h1>
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
                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" :key="error">{{ error }}</p>
                    </div>
                    <div class="control">
                        <button class="button is-fullwidth is-primary">Log in</button>
                    </div>
                </form>
                <hr>
                <router-link to="/sign-up">Sign up</router-link>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: 'LogIn',
    data() {
        return {
            email: '',
            password: '',
            errors: []
        }
    },
    methods: {
        async submitForm() {
            axios.defaults.headers.common['Authorization'] = ''
            localStorage.removeItem('token')
            
            const formData = {
                email: this.email,
                password: this.password
            }
            await axios
                .post('/api/token/login/', formData)
                .then(res => {
                    const token = res.data['auth_token']

                    this.$store.dispatch('setToken', token)
                    axios.defaults.headers.common['Authorization'] = 'Token ' + token
                    localStorage.setItem('token', token)

                })
                .catch(err => {
                    console.log(err.response)
                    if(err.response) {
                        for (const property in err.response.data) {
                            this.errors.push(`${property}: ${err.response.data[property]}`)
                        }
                    } else if(err.message){
                        console.log(JSON.stringify(err.message))
                    } else {
                        console.log(JSON.stringify(err))
                    }
                })
            
            axios
                .get('/api/users/me/')
                .then(res => {
                    const userType = res.data['user_type']
                    const email = res.data['email']
                    this.$store.state.user.userType = userType
                    this.$store.state.user.email = email
                    localStorage.setItem('userType', userType)
                    localStorage.setItem('email', email)
                    this.$router.push('/');
                })
                .catch(err => {
                    console.log(JSON.stringify(err))
                })

        }
    },
}
</script>

<style scoped>
</style>
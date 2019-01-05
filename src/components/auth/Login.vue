<template>
  <div class="login-box">
    <a-form :form="form" @submit="handleSubmit" class='login-form'>
      <a-form-item>
        <a-input
          placeholder='Username'
          v-decorator="[
            'username',
            { rules: [{ required: true, message: 'Please input your username!' }] }
          ]"
        >
          <a-icon slot="prefix" type='user' style="color: rgba(0,0,0,.25)" />
        </a-input>
      </a-form-item>
      <a-form-item>
        <a-input
          v-decorator="[
            'password',
            { rules: [{ required: true, message: 'Please input your password!' }] }
          ]"
          type='password'
          placeholder='Password'
        >
          <a-icon slot="prefix" type='lock' style="color: rgba(0,0,0,.25)" />
        </a-input>
      </a-form-item>
      <a-form-item>
        <!-- <a class='login-form-forgot' href=''>Forgot password</a> -->
        <a-button type='primary' htmlType='submit' class='login-form-button'>
          Log in
        </a-button>
        Or <router-link to='register'>register now!</router-link>
      </a-form-item>
    </a-form>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  beforeCreate () {
    this.form = this.$form.createForm(this)
  },
  methods: {
    handleSubmit (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          axios.post('/api/login', values)
            .then((response) => {
              var data = response.data;
              if (data.status == -1) {
                this.$message.error(data.message);
              } else {
                this.$store.dispatch('setUsername', data.username)
                this.$router.push('/gomoku')
              }
            })
            .catch((error) => {
              this.$message.error(error);
            })
        }
      })
    },
  },
}
</script>
<style>
.login-form-button {
  width: 100%;
}
.login-box {
    width: 50%;
    text-align: center;
    margin: auto;
}
</style>

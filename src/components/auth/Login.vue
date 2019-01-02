<template>
  <div class="login-box">
    <a-form :form="form" @submit="handleSubmit" class='login-form'>
      <a-form-item>
        <a-input
          placeholder='Username'
          v-decorator="[
            'userName',
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
            { rules: [{ required: true, message: 'Please input your Password!' }] }
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
        Or <a href='/register'>register now!</a>
      </a-form-item>
    </a-form>
  </div>
</template>

<script>

export default {
  beforeCreate () {
    this.form = this.$form.createForm(this)
  },
  methods: {
    handleSubmit (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log('Received values of form: ', values)
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

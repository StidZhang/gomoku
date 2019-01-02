<template>
<div class="register-box">
  <a-form @submit="handleSubmit" :form="form">
    <a-form-item>
      <a-input placeholder='Username' v-decorator="[
          'username',
          { rules: [{ required: true, message: 'Please input your username!' }] }
        ]">
        <a-icon slot="prefix" type='user' style="color: rgba(0,0,0,.25)" />
      </a-input>
    </a-form-item>
    <a-form-item>
      <a-input v-decorator="[
          'password',
          { rules: [{
            required: true, message: 'Please input your Password!'
            }, {
              validator: this.validateToNextPassword,
            }]
          }
        ]" type='password' placeholder='Password'>
        <a-icon slot="prefix" type='lock' style="color: rgba(0,0,0,.25)" />
      </a-input>
    </a-form-item>
    <a-form-item>
      <a-input v-decorator="[
          'confirm',
          { rules: [{
            required: true, message: 'Please confirm your Password!'
            }, {
              validator: compareToFirstPassword,
            }]
          }
        ]" type='password' placeholder='Confirm Password'>
        <a-icon slot="prefix" type='lock' style="color: rgba(0,0,0,.25)" />
      </a-input>
    </a-form-item>
    <a-form-item>
      <a-button type='primary' htmlType='submit' class="register-form-button">
        Register
      </a-button>
      Or <router-link to='login'>back to login!</router-link>
    </a-form-item>
  </a-form>
</div>
</template>

<script>
export default {
  beforeCreate() {
    this.form = this.$form.createForm(this)
  },
  methods: {
    handleSubmit(e) {
      e.preventDefault()
      this.form.validateFieldsAndScroll((err, values) => {
        if (!err) {
          console.log('Received values of form: ', values)
        }
      })
    },
    compareToFirstPassword(rule, value, callback) {
      const form = this.form
      if (value && value !== form.getFieldValue('password')) {
        callback('Two passwords that you enter is inconsistent!')
      } else {
        callback()
      }
    },
    validateToNextPassword(rule, value, callback) {
      const form = this.form
      if (value && this.confirmDirty) {
        form.validateFields(['confirm'], {
          force: true
        })
      }
      callback()
    }
  },
}
</script>

<style>
.register-form-button {
  width: 100%;
}
.register-box {
  width: 50%;
  text-align: center;
  margin: auto;
}
</style>

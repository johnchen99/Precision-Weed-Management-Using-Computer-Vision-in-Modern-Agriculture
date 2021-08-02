<template>
  <div>
    <v-app-bar dark color="success">
      <v-btn
        class="ml-2"
        color="white"
        dark
        medium
        icon
        @click="goToLogin_back"
      >
        <v-icon class="mr-2" dark large color="white">
          mdi-chevron-left
        </v-icon>
        Back
      </v-btn>
      <v-spacer></v-spacer>
    </v-app-bar>

    <v-col class="mt-5 text-center">
      <v-avatar size="200" tile color="white" right>
        <img src="@/assets/App_Logo.png" alt="" />
      </v-avatar>
    </v-col>

    <v-col class="text-center">
      <p class="display-1 font-weight-medium">New User?</p>
    </v-col>

    <v-form ref="form" v-model="valid">
      <!-- Username Field -->
      <v-col cols="11" class="ml-4">
        <v-text-field
          v-model="username"
          hint="At least 8 characters"
          label="Username"
          color="green darken-2"
          filled
          rounded
          dense
          clearable
          :rules="[usernameRules.required, usernameRules.minimum]"
          required
          outlined
        ></v-text-field>
      </v-col>
      <!-- Password Field -->
      <v-col cols="11" class="ml-4 mt-n6">
        <v-text-field
          v-model="password"
          hint="At least 8 characters"
          :append-icon="showpassword ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showpassword ? 'text' : 'password'"
          @click:append="showpassword = !showpassword"
          label="Password"
          color="green darken-2"
          filled
          rounded
          dense
          clearable
          :rules="[passwordRules.required, passwordRules.minimum]"
          required
          outlined
          @click="resetPasswordConfirmation"
          @click:clear="resetPasswordConfirmation"
        ></v-text-field>
      </v-col>

      <!-- Confirm Password Field -->
      <v-col cols="11" class="ml-4 mt-n6 mb-3">
        <v-text-field
          v-model="confirm_password"
          hint="At least 8 characters"
          :append-icon="showpassword ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showpassword ? 'text' : 'password'"
          @click:append="showpassword = !showpassword"
          label="Confirm Password"
          color="green darken-2"
          filled
          rounded
          dense
          clearable
          :rules="[
            passwordRules.required,
            passwordRules.minimum,
            passwordRules.match,
          ]"
          required
          outlined
        ></v-text-field>
      </v-col>
    </v-form>

    <!-- Sign Up Button -->
    <v-col cols="11" class="ml-4 mt-n6 mb-3">
      <v-btn
        block
        rounded
        color="success"
        large
        :disabled="!valid"
        @click="signup()"
      >
        Sign Up
      </v-btn>
    </v-col>

    <!-- Snack bar -->
    <v-snackbar
      v-model="snackbar"
      transition="scroll-y-reverse-transition"
      :timeout="2000"
    >
      {{ errmessage }}
      <template v-slot:action="{ attrs }">
        <v-btn color="green" text v-bind="attrs" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "signup",
  data() {
    return {
      msg: "",
      showpassword: false,
      username: "",
      errmessage: "",
      snackbar: false,
      usernameRules: {
        required: (v) => (!!v && !!v.trim()) || "Username is required",
        minimum: (v) => v.length >= 8 || "At least 8 characters",
      },

      password: "",
      confirm_password: "",
      passwordRules: {
        required: (v) => (!!v && !!v.trim()) || "Password is required",
        minimum: (v) => v.length >= 8 || "At least 8 characters",
        match: (v) => v === this.password || "Passwords must match",
      },
      valid: false,
      success: false,
    };
  },
  methods: {
    signup() {
      const path = `http://localhost:5000/signup/${this.username}/${this.password}`;
      axios
        .get(path)
        .then((res) => {
          this.msg = res.data;
          if (this.msg.status.indexOf("Success") !== -1) {
            this.errmessage = "Sign Up Successful";
            this.goToLogin_success();
          } else {
            this.errmessage = "User Exist!";
            this.username = "";
            this.password = "";
            this.confirm_password = "";
            this.$refs.form.reset();
            this.snackbar = true;
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },

    goToLogin_success() {
      this.$router.push({
        name: "login",
        params: {
          previouspage: "Sign Up Successful",
        },
      });
    },

    goToLogin_back() {
      this.$router.push({
        name: "login",
        params: {
          previouspage: "",
        },
      });
    },

    // Reset confirmation password once password is modified
    resetPasswordConfirmation() {
      this.confirm_password = "";
    },
  },

  created() {},
};
</script>

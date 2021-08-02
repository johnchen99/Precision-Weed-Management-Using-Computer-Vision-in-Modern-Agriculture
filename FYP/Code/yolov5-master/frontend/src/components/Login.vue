<template>
  <div class="text-center">
    <v-app-bar color="white" flat>
      <v-progress-linear
        :active="loading"
        :indeterminate="loading"
        absolute
        top
        color="green"
      ></v-progress-linear>
    </v-app-bar>

    <v-col class="mt-5">
      <v-avatar size="200" tile color="white" right @click="clickLogo">
        <img src="@/assets/App_Logo.png" alt="" />
      </v-avatar>
    </v-col>
    <v-col>
      <p class="display-1 font-weight-medium">Welcome Back!</p>
    </v-col>
    <v-col class="mt-n10">
      <p class="caption" v-if="nowtime">Current Time: {{ nowtime }}</p>
      <p class="caption white--text" v-else>.</p>
    </v-col>
    <v-form ref="form" v-model="valid">
      <!-- Username Field -->
      <v-col cols="11" class="ml-4">
        <v-text-field
          v-model="username"
          label="Username"
          color="green darken-2"
          filled
          rounded
          dense
          clearable
          :rules="usernameRules"
          required
          outlined
        ></v-text-field>
      </v-col>

      <!-- Password Field -->
      <v-col cols="11" class="ml-4 mt-n6 mb-3">
        <v-text-field
          v-model="password"
          label="Password"
          color="green darken-2"
          :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
          :type="show ? 'text' : 'password'"
          @click:append="show = !show"
          filled
          rounded
          dense
          clearable
          :rules="passwordRules"
          required
          outlined
        ></v-text-field>
      </v-col>
    </v-form>

    <!-- Login button -->
    <v-col cols="11" class="ml-4 mt-n6 mb-3">
      <v-btn
        block
        rounded
        color="success"
        large
        :disabled="!valid"
        @click="login"
      >
        Login
      </v-btn>
    </v-col>

    <!-- Sign Up Button -->
    <v-col cols="11" class="ml-4 mt-n6 mb-3">
      <v-btn block rounded color="success" large @click="signup">
        Sign Up
      </v-btn>
    </v-col>

    <!-- Snack bar -->
    <v-snackbar
      transition="scroll-y-reverse-transition"
      v-model="snackbar"
      :timeout="2000"
    >
      {{ snackbar_text }}
      <template v-slot:action="{ attrs }">
        <v-btn color="green" text v-bind="attrs" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>

    <v-footer padless absolute>
      <v-col class="teal darken-4 py-0 text-center white--text" cols="12">
        {{ new Date().getFullYear() }} — <strong>TP045873</strong>
      </v-col>
    </v-footer>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "login",
  props: ["previouspage"],
  data() {
    return {
      msg: "",
      snackbar_text: "",
      snackbar: false,
      errmessage: "",
      username: "",
      nowtime: "",
      interval: null,
      show: false,
      loading: false,
      usernameRules: [(v) => (!!v && !!v.trim()) || "Username is required"],

      password: "",
      passwordRules: [(v) => (!!v && !!v.trim()) || "Password is required"],
      incorrect: false,
      valid: false,
    };
  },
  methods: {
    login() {
      const path = `http://localhost:5000/login/${this.username}/${this.password}`;
      axios
        .get(path)
        .then((res) => {
          this.msg = res.data;
          if (this.msg.Status.indexOf("Success") !== -1) {
            this.goToMenu();
          } else if (this.msg.Status.indexOf("Incorrect Password") !== -1) {
            this.snackbar_text = "Incorrect Password";
            this.snackbar = true;
            this.password = "";
          } else {
            this.snackbar_text = "User does not exist";
            this.snackbar = true;
            this.$refs.form.reset();
            this.username = "";
            this.password = "";
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },

    goToMenu() {
      this.$router.push({
        name: "main_menu",
        params: {
          userId: this.msg.UserId,
          previouspage: "Login",
          num: NaN,
        },
      });
    },

    signup() {
      this.$router.push("/signup");
    },

    clickLogo() {
      this.snackbar_text = "Welcome Back !";
      this.snackbar = true;
    },

    current_time() {
      this.interval = setInterval(() => {
        this.nowtime = Intl.DateTimeFormat("en-US", {
          hour: "numeric",
          minute: "numeric",
          second: "numeric",
        }).format();
      }, 1000);
    },
  },

  created() {
    this.loading = true;
    this.current_time();
    console.log("Previous Page: ", this.previouspage);
    if (this.previouspage == "Sign Up Successful") {
      this.snackbar_text = "Signup Successful !";
      this.snackbar = true;
    } else if (this.previouspage == "Log Out Successful") {
      this.snackbar_text = "Logout Successful !";
      this.snackbar = true;
    }
  },

  watch: {
    loading(val) {
      if (!val) return;
      setTimeout(() => (this.loading = false), 900);
    },
  },

  beforeDestroy() {
    // Prevent memory leak
    clearInterval(this.interval);
  },
};
</script>

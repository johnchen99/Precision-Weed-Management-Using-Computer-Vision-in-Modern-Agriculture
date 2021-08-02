<template>
  <div>
    <v-app-bar dark color="success" app>
      <v-btn color="black" dark medium icon @click="logout_successful">
        <v-icon dark large color="white"> mdi-logout </v-icon>
      </v-btn>

      <v-spacer></v-spacer>
      <v-toolbar-title class="text-center">Tasks</v-toolbar-title>
      <v-spacer></v-spacer>

      <v-btn color="black" dark medium icon @click="goToHistory()">
        <v-icon dark large color="white"> mdi-history </v-icon>
      </v-btn>
    </v-app-bar>

    <!-- Main content -->
    <v-col v-for="(item, i) in items" :key="i" cols="12">
      <v-card color="white" class="rounded-lg" @click="openDialog(item)">
        <div class="d-flex flex-no-wrap justify-space-between">
          <div>
            <v-card-title
              class="headline"
              v-text="item.Gridname"
            ></v-card-title>

            <v-card-subtitle v-text="item.Crop"></v-card-subtitle>
            <v-card-subtitle class="font-weight-normal pt-8 pb-0"
              >Last updated:
            </v-card-subtitle>
            <v-card-subtitle class="font-weight-normal mt-n6">
              {{ new Date().toLocaleString("en-GB") }}
            </v-card-subtitle>
          </div>

          <v-avatar class="ma-3" size="140" tile>
            <img :src="require(`@/assets/Images/${item.Src}`)" />
          </v-avatar>
        </div>
      </v-card>
    </v-col>

    <!-- Snack bar -->
    <v-snackbar
      v-model="snackbar"
      transition="scroll-y-reverse-transition"
      :timeout="2000"
    >
      {{ snackbar_text }}
      <template v-slot:action="{ attrs }">
        <v-btn color="green" text v-bind="attrs" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>

    <!-- Confirmation dialog -->
    <v-dialog
      scrollable
      @click:outside="closeDialog"
      v-if="selected"
      v-model="dialog"
      width="500"
      max-height="300"
    >
      <v-card>
        <v-card-title class="pl-3 success white--text">
          Process - {{ selected.Gridname }}
        </v-card-title>
        <v-avatar class="ma-3" size="303" tile v-if="!processed">
          <img :src="require(`@/assets/Images/${selected.Src}`)" />
        </v-avatar>
        <v-avatar class="ma-3" size="303" tile v-else>
          <img :src="require(`@/assets/exp/Processed_Temp.png`)" />
        </v-avatar>
        <v-card-title
          v-if="processed == true && no_detect == false"
          class="ml-n3 pt-0"
        >
          Target Coordinates (Weed):
        </v-card-title>
        <v-card flat class="px-4 scroll" v-if="processed">
          <p v-for="(midpoint, i) in midpoints" :key="i">
            {{ i + 1 }}. ({{ midpoint }})
          </p>
        </v-card>
        <v-divider></v-divider>
        <v-card-actions v-if="!processed">
          <v-spacer></v-spacer>
          <v-btn color="error" text @click="dialog = false"> Cancel </v-btn>

          <v-btn v-if="!processing" color="success" text @click="processImage">
            PROCEED
          </v-btn>
          <v-btn v-else text disabled> PROCEED </v-btn>
        </v-card-actions>
        <v-card-actions v-else>
          <v-spacer></v-spacer>
          <v-btn color="error" text @click="closeDialog()"> Cancel </v-btn>
          <v-btn
            @click="finishProcess(selected)"
            color="success"
            text
            v-if="no_detect == false"
          >
            SUBMIT to Remover
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "main_menu",
  props: ["userId", "previouspage", "rand_num"],
  data() {
    return {
      msg: "",
      snackbar_text: "",
      fab: false,
      snackbar: false,
      random_number_array: [],
      items: [],
      dialog: false,
      selected: null,
      processed: false,
      processing: false,
      midpoints: [],
      no_detect: false,
      scrollingTop: false,
    };
  },
  methods: {
    logout_successful() {
      this.$router.push({
        name: "login",
        params: {
          previouspage: "Log Out Successful",
        },
      });
    },

    // Preventive measure
    logout_force() {
      this.$router.push("/login");
    },

    onScroll(e) {
      if (typeof window === "undefined") return;
      const top = window.pageYOffset || e.target.scrollTop || 0;
      this.fab = top > 20;
    },
    
    goToHistory() {
      this.$router.push({
        name: "history",
        params: {
          userId: this.userId,
          rand_num: this.random_number_array,
        },
      });
    },

    // Scroll back to the top
    toTop() {
      this.scrollingTop = true;
      this.$vuetify.goTo(0);
      this.scrollingTop = false;
    },

    openDialog(item) {
      if (!this.scrollingTop) {
        this.selected = item;
        this.processed = false;
        this.dialog = true;
        document.activeElement.blur();
      }
    },

    // Obtain grid number from DB, randomly assign photo
    createItemList(randomnumber) {
      const path = `http://localhost:5000/main_menu`;
      axios
        .get(path)
        .then((res) => {
          this.items = res.data;
          let i = 0;
          if (!randomnumber)
            for (i = 0; i < this.items.length; i++) {
              let randomNumber = Math.random() * 60;
              if (randomNumber < 1) {
                randomNumber = 1;
              }
              this.random_number_array.push(Math.round(randomNumber));
            }
          else {
            this.random_number_array = randomnumber;
          }

          for (i = 0; i < this.items.length; i++) {
            if (this.random_number_array[i] < 10) {
              this.items[i].Src =
                "00" + this.random_number_array[i] + "_image.png";
            }
            if (this.random_number_array[i] > 9) {
              this.items[i].Src =
                "0" + this.random_number_array[i] + "_image.png";
            }
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },

    processImage() {
      this.no_detect = true;
      this.processing = true;
      const path = `http://localhost:5000/detect/${this.selected.Src}`;
      axios
        .get(path)
        .then((res) => {
          console.log(res);
          let i = 0;
          for (i = 0; i < res.data.length; i++) {
            this.midpoints.push(res.data[i]);
          }
          if (!this.midpoints) {
            this.no_detect = true;
          } else {
            this.no_detect = false;
          }
          this.processed = true;
        })
        .catch((error) => {
          console.error(error);
        });
      this.processing = false;
    },

    finishProcess(item) {
      this.dialog = false;
      this.processed = false;

      console.log(item);
      let filtername = item.Gridname;
      this.items = this.items.filter((grid) => grid.Gridname != filtername);
      this.snackbar_text = "Task Submitted !";
      this.snackbar = true;

      // Post history to DB
      let midpoint_string = this.midpoints.toString();

      const path = `http://localhost:5000/post_history/${this.userId}/${item.GridID}/${midpoint_string}`;
      axios
        .get(path)
        .then((res) => {
          this.msg = res.data;
          if (this.msg.indexOf("Success") !== -1) {
            console.log("Midpoints Successfully Sent to Remover.");
          }
        })
        .catch((error) => {
          console.error(error);
        });
      this.midpoints = [];
    },

    closeDialog() {
      this.dialog = false;
      this.midpoints = [];
    },
  },

  created() {
    if (!this.userId) {
      console.log("Back to Login Page");
      this.logout_force();
    } else if (this.previouspage != "history") {
      this.snackbar_text = "Login Successful !";
      this.snackbar = true;
    }
    this.createItemList(this.rand_num);
  },
};
</script>

<style>

/* Enable scroll for midpoints */
.scroll {
  overflow-y: scroll;
}
</style>

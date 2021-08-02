<template>
  <div>
    <v-app-bar dark color="success" app>
      <v-btn color="black" dark medium icon @click="goToMenu">
        <v-icon dark large color="white"> mdi-chevron-left </v-icon>
      </v-btn>

      <v-spacer></v-spacer>
      <v-toolbar-title class="text-center">My History</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="black" dark medium icon @click="inverse_list">
        <v-icon dark medium color="white"> mdi-arrow-up-down </v-icon>
      </v-btn>
    </v-app-bar>

    <!-- Main content -->
    <v-col v-for="(item, i) in items" :key="i" cols="12">
      <v-card color="white" class="rounded-lg">
        <v-expansion-panels>
          <v-expansion-panel>
            <v-expansion-panel-header>
              <v-row no-gutters>
                <v-col cols="5"> <b>Task:</b> Grid {{ item.GridID }} </v-col>
                <v-col cols="7" class="text--secondary">
                  {{ item.Record_Time }}
                </v-col>
              </v-row>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-row no-gutters><b>Midpoints (Weed):</b> </v-row>
              <v-row no-gutters v-for="(point, i) in item.Midpoint" :key="i">
                {{ i + 1 }}. ({{ point[0] }}, {{ point[1] }})
              </v-row>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>

        <!-- Scroll Up Button -->
        <v-btn
          v-scroll="onScroll"
          v-show="fab"
          fab
          dark
          fixed
          bottom
          elevation="2"
          right
          color="success"
          @click="toTop"
        >
          <v-icon>mdi-chevron-up</v-icon>
        </v-btn>
      </v-card>
    </v-col>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "login",
  props: ["userId", "rand_num"],
  data() {
    return {
      fab: false,
      items: "",
      show: false,
    };
  },
  methods: {
    getHistory() {
      const path = `http://localhost:5000/get_history/${this.userId}`;
      axios
        .get(path)
        .then((res) => {
          this.items = res.data;
          let index = 0,
            index2 = 0,
            index3 = 0;
          for (index = 0; index < this.items.length; index++) {
            // Convert UTC Time into local time
            let theDate = new Date(Date.parse(this.items[index].Record_Time));
            this.items[index].Record_Time = theDate.toLocaleString("en-GB");
            this.items[index].Midpoint = this.chunkArray(
              this.items[index].Midpoint,
              2
            );

            // Limit number of decimals
            for (
              index2 = 0;
              index2 < this.items[index].Midpoint.length;
              index2++
            ) {
              for (
                index3 = 0;
                index3 < this.items[index].Midpoint[index2].length;
                index3++
              ) {
                this.items[index].Midpoint[index2][index3] = parseFloat(
                  this.items[index].Midpoint[index2][index3].trim()
                ).toFixed(5);
              }
            }
          }

          // Rearrange array into decending order
          this.items.reverse();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },

    // Split midpoint array into pairs
    chunkArray(myArray, chunk_size) {
      let index = 0;
      let arrayLength = myArray.length;
      let tempArray = [];

      for (index = 0; index < arrayLength; index += chunk_size) {
        let myChunk = myArray.slice(index, index + chunk_size);
        tempArray.push(myChunk);
      }
      return tempArray;
    },

    goToMenu() {
      this.$router.push({
        name: "main_menu",
        params: {
          userId: this.userId,
          previouspage: "history",
          rand_num: this.rand_num,
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

    // Scroll back to the top
    toTop() {
      this.$vuetify.goTo(0);
    },

    // Inverse order of history
    inverse_list() {
      this.items.reverse();
    },
  },

  created() {
    console.log("ID:", this.userId);
    if (!this.userId) {
      console.log("Back to Login Page");
      this.logout_force();
    }
    this.getHistory();
  },
};
</script>

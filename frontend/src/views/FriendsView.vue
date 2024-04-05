<template>
  <div>
    <div class="container-md">
      <h1 class="my-4">Freunde</h1>
    </div>
    <div class="container-md bg-body-secondary py-3 rounded">
      <h2 class="mb-4">Freunde hinzufügen</h2>
      <form class="form-inline my-2 my-lg-0">
        <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search" v-model="searchQuery">
      </form>
      <div v-if="filteredUsers[0]" class="container-md bg-body-tertiary rounded py-2">
        <ul  class="px-0 my-0">
          <li v-for="user in filteredUsers" :key="user.id" class="row align-items-center py-3 gy-2 gy-lg-0">
            <RouterLink :to="{ name: 'friendProfile', params: { id: user.id } }" class="col-lg-2 link-primary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover">{{user.username}}</RouterLink>
            <div class="col-3 col-lg align-self-end d-flex  justify-content-lg-end d-flex-column">
              <button @click="addFriend(user.id)" class="btn btn-success btn-block">Hinzufügen</button>
            </div>
          </li>
        </ul>
      </div>
    </div>
    <div class="container-md bg-body-secondary py-3 rounded mt-4">
      <h2 class="mb-4">Meine Freunde</h2>
      <div v-if="!friends[0]">Du hast im Moment keine Freunde.</div>
      <div v-if="friends[0]" class="container-md bg-body-tertiary rounded py-2">
        <ul class="px-0 my-0">
          <li v-for="friend in friends" :key="friend.user_id" class="row align-items-center py-3 gy-2 gy-lg-0">
            <RouterLink :to="{ name: 'friendProfile', params: { id: friend.user_id } }" class="col-lg-2 link-primary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover">{{friend.username}}</RouterLink>
            <div class="col-3 col-lg align-self-end d-flex  justify-content-lg-end d-flex-column">
              <button class="btn btn-danger" @click="deleteFriend(friend.user_id)">Entfernen</button>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
import friendshipService from "../services/friendship.service";
import userService from "../services/user.service";
import { ref, computed } from "vue";
import { useStore } from "../stores/store";

const store = useStore();
const friends = ref([]);
const allUsers = ref([]);
const searchQuery = ref("");
const filteredUsers = computed(() => {
  if (searchQuery.value.length >= 1) {
    const query = searchQuery.value.toLowerCase();
    return allUsers.value.filter(user => {
      const isMatch = user.username.toLowerCase().includes(query);
      const isNotOwnUsername = user.username !== store.user.username;
      return isMatch && isNotOwnUsername;
    });
  }
  return allUsers;
})

async function getFriends() {
  try {
    const response = await friendshipService.getFriend(store.user.id);
    if (response.status == 200) {
      friends.value = response.data;
    }
  } catch (error) {
    console.log(error);
  }
}

async function getAllUsers() {
  try {
    const response = await userService.getUsers();
    if (response.status == 200) {
      allUsers.value = response.data;
    }
  } catch (error) {
    console.log(error);
  }
}

async function addFriend(friendId) {
  try {
    const response = await friendshipService.addFriend(store.user.id, friendId);
    if (response.status == 200) {
      getFriends();
    }
  } catch (error) {
    console.log(error);
  }
}

async function deleteFriend(friendId) {
  try {
    const response = await friendshipService.deleteFriend(store.user.id, friendId);
    if (response.status == 204) {
      getFriends();
    }
  } catch (error) {
    console.log(error);
  }
}

getFriends();
getAllUsers();
</script>
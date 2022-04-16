<template>
    <main class="container">
        <p>Home</p>
    </main>
</template>

<script setup>
import { onMounted } from 'vue';
import { useUserStore } from '../store/user';
// onMounted(() => {
//     const userStore = useUserStore();
//     console.log(userStore.getToken);
// });
</script>

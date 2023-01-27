<template>
  <div>
    <vue-json-pretty :showLineNumber="true" :editable="true" :data="{ key: 'value' }" />
  </div>
</template>

<script>
import VueJsonPretty from 'vue-json-pretty';
import 'vue-json-pretty/lib/styles.css';

export default {
  components: {
    VueJsonPretty
  }
};
</script>

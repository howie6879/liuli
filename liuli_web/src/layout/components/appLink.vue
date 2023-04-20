<template>
  <component :is="type" v-bind="linkProps(to)">
    <slot />
  </component>
</template>

<script setup lang="ts">
import { isExternal as checkIsisExternal } from '@/utils';
import { computed } from 'vue';

const props = defineProps({
  to: {
    type: String,
    required: true
  }
});
// 是否网络链接
const isExternal = computed(() => checkIsisExternal(props.to));
// 根据传入的url决定渲染哪种组件
const type = computed(() => {
  if (isExternal.value) {
    return 'a';
  }
  return 'router-link';
});

// 根据传入的url决定渲染哪种组件
function linkProps(to: any) {
  if (isExternal.value) {
    return {
      href: to,
      target: '_blank',
      rel: 'noopener'
    };
  }
  return { to: to };
}
</script>

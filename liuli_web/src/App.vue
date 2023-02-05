<template>
  <router-view></router-view>
</template>

<script>
import './style/common.scss';
import './style/global.scss';
export default {
  name: 'App'
};
</script>
<style lang="scss">
:root {
  --block-spacing-vertical: 0rem !important;
  --el-header-padding: 0px !important;

}

a {
  text-decoration: none;
}

.el-header {
  padding: 0;

}

.el-menu {
  border-right: 0px !important;

}

div,
section {
  margin-bottom: 0px;
  box-sizing: border-box;
}
</style>
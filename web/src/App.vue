<template>
  <div id="app" class="container">
    <nav-bar></nav-bar>
    <search></search>
    <novel-list></novel-list>
  </div>
</template>

<script>
import NovelList from './components/NovelList'
import Search from './components/Search'
import NavBar from './components/NavBar'
import store from './vuex/store'

export default {
  components: {
    NavBar,
    Search,
    NovelList
  },
  store
}
</script>

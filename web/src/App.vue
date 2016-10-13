<template>
  <div id="app" class="container">
    <nav_bar></nav_bar>
    <search></search>
    <novel_list></novel_list>
  </div>
</template>

<script>
import NovelList from './components/NovelList'
import Search from './components/Search'
import NavBar from './components/NavBar'

export default {
  methods: {

  },
  components: {
    nav_bar: NavBar,
    search: Search,
    novel_list: NovelList
  }
}
</script>

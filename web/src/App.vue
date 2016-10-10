<template>
  <div id="app">
    <search></search>
    <novel_list :novels.sync="novels"></novel_list>
  </div>
</template>

<script>
import NovelList from './components/NovelList'
import Search from './components/Search'

export default {
  data(){
    return {
      novels: []
    }
  },
  methods: {

  },
  components: {
    search: Search,
    novel_list: NovelList
  }
}
</script>

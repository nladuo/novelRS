/**
 * Created by kalen on 10/11/16.
 */

import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const state = {
  novels: [],
  newSearch: ""
};

const mutations = {
  SEARCH_NOVELS (state, name) {
    state.novels = [{
      name: name,
      author: 'test',
      category: 'test',
      word_num: 'test',
      similarity: 'test'
    }]
  }
};


export default new Vuex.Store({
  state,
  mutations
});

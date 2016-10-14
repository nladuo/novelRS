/**
 * Created by kalen on 10/14/16.
 */

export const searchNovels = ({ dispatch }, novel_name) => {
  dispatch('SEARCH_NOVELS', novel_name)
};

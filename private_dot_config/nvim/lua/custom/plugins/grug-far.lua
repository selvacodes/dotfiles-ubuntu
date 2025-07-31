return {
  'MagicDuck/grug-far.nvim',
  config = function()
    require('grug-far').setup {
      engine = 'ripgrep',
      keymaps = {
        ['<leader>f'] = 'grug-far',
        ['<leader>F'] = 'grug-far-clear',
      },
    }
  end,
}

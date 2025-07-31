return {
  'stevearc/overseer.nvim',
  config = function()
    require('overseer').setup {
      parsers = {
        'npm', -- Enable npm parser
      },
    }
  end,
}

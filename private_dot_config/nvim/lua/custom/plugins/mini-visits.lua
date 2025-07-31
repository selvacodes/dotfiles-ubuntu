local M = {
  'echasnovski/mini.visits',
  version = false,
  config = function()
    local mini_visits = require 'mini.visits'
    -- vim.opt.laststatus = 3

    local opts = {
      -- your configuration comes here
      -- or leave it empty to use the default settings
      -- refer to the configuration section below
    }
    mini_visits.setup(opts)
  end,
}

return M

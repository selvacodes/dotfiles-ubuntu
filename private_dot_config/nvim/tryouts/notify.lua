local M = {
  'rcarriga/nvim-notify',
  keys = {
    {
      '<leader>u',
      function()
        require('notify').dismiss { silent = true, pending = true }
      end,
    },
  },
  config = function()
    local notify = require 'notify'
    notify.setup {
      background_colour = '#808080',
      fps = 30,
      timeout = 500,
      top_down = false
    }
    vim.notify = notify
  end,
}
return M

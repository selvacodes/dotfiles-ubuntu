-- return {
--   {
--     'kevinhwang91/nvim-ufo',
--     dependencies = {
--       'kevinhwang91/promise-async',
--       'kevinhwang91/promise-async-tests',
--     },
--     config = function()
--       require('ufo').setup()
--
--       vim.o.foldcolumn = '1' -- '0' is not bad
--       vim.o.foldlevel = 99 -- Using ufo provider need a large value, feel free to decrease the value
--       vim.o.foldlevelstart = 99
--       vim.o.foldenable = true
--
--       -- Using ufo provider need remap `zR` and `zM`. If Neovim is 0.6.1, remap yourself
--       vim.keymap.set('n', 'zR', require('ufo').openAllFolds)
--       vim.keymap.set('n', 'zN', require('ufo').openAllFolds)
--       vim.keymap.set('n', 'zM', require('ufo').closeAllFolds)
--     end,
--   },
-- }
return {
  'kevinhwang91/nvim-ufo',
  dependencies = 'kevinhwang91/promise-async',
  event = 'VeryLazy',
  opts = {
    open_fold_hl_timeout = 400,
    preview = {
      win_config = {
        border = { '', '─', '', '', '', '─', '', '' },
        winblend = 0,
      },
      mappings = {
        scrollU = '<C-u>',
        scrollD = '<C-d>',
        jumpTop = '[',
        jumpBot = ']',
      },
    },
  },
  config = function(_, opts)
    local handler = function(virtText, lnum, endLnum, width, truncate)
      local newVirtText = {}
      local totalLines = vim.api.nvim_buf_line_count(0)
      local foldedLines = endLnum - lnum
      local suffix = ('  %d %d%%'):format(foldedLines, foldedLines / totalLines * 100)
      local sufWidth = vim.fn.strdisplaywidth(suffix)
      local targetWidth = width - sufWidth
      local curWidth = 0
      for _, chunk in ipairs(virtText) do
        local chunkText = chunk[1]
        local chunkWidth = vim.fn.strdisplaywidth(chunkText)
        if targetWidth > curWidth + chunkWidth then
          table.insert(newVirtText, chunk)
        else
          chunkText = truncate(chunkText, targetWidth - curWidth)
          local hlGroup = chunk[2]
          table.insert(newVirtText, { chunkText, hlGroup })
          chunkWidth = vim.fn.strdisplaywidth(chunkText)
          if curWidth + chunkWidth < targetWidth then
            suffix = suffix .. (' '):rep(targetWidth - curWidth - chunkWidth)
          end
          break
        end
        curWidth = curWidth + chunkWidth
      end
      local rAlignAppndx = math.max(math.min(vim.opt.textwidth['_value'], width - 1) - curWidth - sufWidth, 0)
      suffix = (' '):rep(rAlignAppndx) .. suffix
      table.insert(newVirtText, { suffix, 'MoreMsg' })
      return newVirtText
    end
    opts['fold_virt_text_handler'] = handler
    require('ufo').setup(opts)
    vim.o.fillchars = [[eob: ,fold: ,foldopen:▾,foldsep: ,foldclose:▸]]
    vim.o.foldcolumn = 'auto:2' -- 10 breaks the plugin, 9 works with the issue mentioned before
    vim.o.foldnestmax = 1
    vim.o.foldlevel = 99999999 -- Bigger than this also breaks the plugin
    vim.o.foldlevelstart = 99999999
    vim.o.foldenable = true

    vim.o.scrolloff = 5
    vim.o.sidescrolloff = 5

    -- Redrawing and cursor enhancements
    vim.o.lazyredraw = false
    vim.o.cursorline = true
    vim.o.cursorcolumn = true
    vim.o.cursorlineopt = 'number,line'
    vim.fn.sign_define('FoldClosed', { text = '▸', texthl = 'Folded' })
    vim.fn.sign_define('FoldOpen', { text = '▾', texthl = 'Folded' })
    vim.fn.sign_define('FoldSeparator', { text = ' ', texthl = 'Folded' })
    vim.keymap.set('n', 'K', function()
      local winid = require('ufo').peekFoldedLinesUnderCursor()
      if not winid then
        -- choose one of coc.nvim and nvim lsp
        vim.lsp.buf.hover()
      end
    end)
  end,
}

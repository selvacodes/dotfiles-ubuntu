local M = {
	"echasnovski/mini.visits",
	version = false,
	config = function()
		local mini_visits = require("mini.visits")
		local opts = {}
		mini_visits.setup(opts)
	end,
}

return M

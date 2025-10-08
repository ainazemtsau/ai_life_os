# не эхо-ить сами команды make
.SILENT: fmt fix lint typecheck test qa ci

PNPM = pnpm --silent
SUCCESS_MSG ?= ✅ всё ок

fmt:
	$(PNPM) run format >/dev/null  # прячем обычный вывод, оставляем только stderr

fix:
	$(PNPM) run lint:fix

lint:
	$(PNPM) run lint

typecheck:
	$(PNPM) run typecheck

test:
	$(PNPM) run test

qa:
	@set -e; \
	$(PNPM) run format >/dev/null; \
	$(PNPM) run lint:fix; \
	$(PNPM) run lint; \
	$(PNPM) run typecheck; \
	$(PNPM) run test; \
	echo "$(SUCCESS_MSG)"

ci:
	@set -e; \
	$(PNPM) run format:check >/dev/null; \
	$(PNPM) run lint; \
	$(PNPM) run typecheck; \
	echo "$(SUCCESS_MSG)"

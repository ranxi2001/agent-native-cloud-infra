PYTHON ?= python3
CODEX_HOME ?= $(HOME)/.codex
SKILL_VALIDATOR ?= $(CODEX_HOME)/skills/.system/skill-creator/scripts/quick_validate.py

.PHONY: test validate-skills doctor whitespace check

test:
	$(PYTHON) -m unittest discover -s tests -v

validate-skills:
	@for skill in .agents/skills/*; do \
		$(PYTHON) $(SKILL_VALIDATOR) "$$skill" || exit 1; \
	done
	$(PYTHON) scripts/validate_skills.py

doctor:
	./workstation doctor

whitespace:
	$(PYTHON) scripts/check_whitespace.py

check: test validate-skills doctor whitespace

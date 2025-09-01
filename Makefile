.PHONY: help install test test-local lint format build clean docs publish-test publish

# Variables
PYTHON_VERSION = 3.11
PACKAGE_NAME = langpify

help: ## Mostrar ayuda de comandos disponibles
	@echo "Comandos disponibles para $(PACKAGE_NAME):"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instalar dependencias del proyecto
	@echo "🔧 Instalando dependencias..."
	poetry env use python$(PYTHON_VERSION)
	poetry install
	@echo "✅ Dependencias instaladas"

test: ## Ejecutar tests completos (requiere OPENAI_API_KEY)
	@echo "🧪 Ejecutando tests completos..."
	poetry run python tests/test.py
	@echo "✅ Tests completados"

lint: ## Ejecutar linting del código
	@echo "🔍 Ejecutando linting..."
	poetry run flake8 src/ tests/
	poetry run mypy src/
	@echo "✅ Linting completado"

format: ## Formatear código con black e isort
	@echo "🎨 Formateando código..."
	poetry run black src/ tests/
	poetry run isort src/ tests/
	@echo "✅ Código formateado"

build: ## Construir el paquete
	@echo "📦 Construyendo paquete..."
	poetry build
	@echo "✅ Paquete construido en dist/"

clean: ## Limpiar archivos temporales y build
	@echo "🧹 Limpiando archivos temporales..."
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	@echo "✅ Limpieza completada"

docs: ## Generar documentación
	@echo "📚 Generando documentación..."
	cd docs && poetry run make html
	@echo "✅ Documentación generada en docs/_build/html/"

publish-test: build ## Publicar en TestPyPI
	@echo "🚀 Publicando en TestPyPI..."
	poetry config repositories.testpypi https://test.pypi.org/legacy/
	poetry publish -r testpypi
	@echo "✅ Publicado en TestPyPI"

publish: build ## Publicar en PyPI
	@echo "🚀 Publicando en PyPI..."
	poetry publish
	@echo "✅ Publicado en PyPI"

dev-setup: install ## Configuración completa para desarrollo
	@echo "⚙️  Configurando entorno de desarrollo..."
	poetry run pre-commit install || echo "pre-commit no disponible"
	@echo "✅ Entorno de desarrollo configurado"

check: lint test-local ## Ejecutar checks completos (lint + test local)
	@echo "✅ Todos los checks pasaron"

# Comandos de desarrollo rápido
run-test: test-local ## Alias para test-local
run: test-local ## Alias para test-local

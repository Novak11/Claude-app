"""
Questionnaire Builder
Loads templates and generates customized questionnaires based on meta-answers
"""

import yaml
from pathlib import Path
from typing import Dict, List, Any

class QuestionnaireBuilder:
    """Builds customized questionnaires based on user preferences"""

    def __init__(self, templates_dir: str = "templates/questions"):
        self.templates_dir = Path(templates_dir)
        self.templates = {}
        self._load_templates()

    def _load_templates(self):
        """Load all YAML question templates"""
        for template_file in self.templates_dir.glob("*.yaml"):
            template_name = template_file.stem
            with open(template_file, 'r') as f:
                self.templates[template_name] = yaml.safe_load(f)

    def select_template(self, detail_level: str) -> Dict[str, Any]:
        """
        Select template based on detail level

        Args:
            detail_level: 'minimal', 'moderate', or 'deep'

        Returns:
            Template dictionary
        """
        template_map = {
            'minimal': 'minimal',
            'moderate': 'moderate',
            'deep': 'deep'
        }

        template_name = template_map.get(detail_level.lower(), 'moderate')
        return self.templates.get(template_name, self.templates['moderate'])

    def filter_questions(self, template: Dict[str, Any], meta_answers: Dict[str, Any]) -> Dict[str, Any]:
        """
        Filter questions based on meta-questionnaire answers

        Args:
            template: Full template dictionary
            meta_answers: User's meta-questionnaire responses

        Returns:
            Filtered template with relevant questions only
        """
        filtered_template = {
            'metadata': template['metadata'],
            'categories': {}
        }

        # Filter based on priority and user selections
        selected_aspects = meta_answers.get('key_aspects', [])

        for category_name, category_data in template['categories'].items():
            # Always include high priority categories
            if category_data.get('priority') == 'high':
                filtered_template['categories'][category_name] = category_data
            # Include if user selected this aspect
            elif self._category_matches_aspect(category_name, selected_aspects):
                filtered_template['categories'][category_name] = category_data

        return filtered_template

    def _category_matches_aspect(self, category: str, aspects: List[str]) -> bool:
        """Check if category matches user-selected aspects"""
        aspect_mapping = {
            'technical': ['technical_background', 'problem_solving'],
            'career': ['career_context', 'values_philosophy'],
            'communication': ['communication_preferences'],
            'geographic': ['geographic_context'],
            'work_patterns': ['work_patterns', 'detailed_work_patterns'],
        }

        for aspect in aspects:
            if category in aspect_mapping.get(aspect, []):
                return True
        return False

    def generate_markdown(self, template: Dict[str, Any]) -> str:
        """
        Generate questionnaire.md file content

        Args:
            template: Filtered template dictionary

        Returns:
            Markdown content as string
        """
        md_lines = []

        # Header
        md_lines.append("# AI-Brain Integration: Your Core Identity Questionnaire\n")
        md_lines.append(f"**Profile Type:** {template['metadata']['name']}\n")
        md_lines.append(f"**Description:** {template['metadata']['description']}\n")
        md_lines.append(f"**Estimated Time:** {template['metadata']['estimated_time']}\n")
        md_lines.append("---\n\n")

        md_lines.append("## Instructions\n\n")
        md_lines.append("Complete this questionnaire to create your personalized AI memory system.\n\n")
        md_lines.append("- Answer each question thoughtfully\n")
        md_lines.append("- Use these answers to create your `core-identity.md` file\n")
        md_lines.append("- See `setup-instructions.md` for implementation steps\n\n")
        md_lines.append("---\n\n")

        # Questions by category
        for category_name, category_data in template['categories'].items():
            # Format category name
            display_name = category_name.replace('_', ' ').title()
            md_lines.append(f"## {display_name}\n\n")

            for question in category_data['questions']:
                md_lines.append(f"**Q{question['id']}:** {question['question']}\n\n")

                if question['type'] == 'multiple_choice':
                    for option in question['options']:
                        md_lines.append(f"- [ ] {option}\n")
                    md_lines.append("\n")
                elif question['type'] == 'short_text':
                    placeholder = question.get('placeholder', 'Your answer here')
                    md_lines.append(f"*{placeholder}*\n\n")
                    md_lines.append("**Your answer:**\n\n")
                    md_lines.append("_____________________________________________\n\n")
                elif question['type'] == 'ranking':
                    md_lines.append("Rank the following (1 = highest priority):\n\n")
                    for i, option in enumerate(question['options'], 1):
                        md_lines.append(f"- [ ] {option} (Rank: ___)\n")
                    md_lines.append("\n")

                md_lines.append("---\n\n")

        return ''.join(md_lines)

    def build(self, meta_answers: Dict[str, Any]) -> str:
        """
        Main method: Build complete questionnaire

        Args:
            meta_answers: Dictionary of meta-questionnaire responses

        Returns:
            questionnaire.md content as string
        """
        # Select template based on detail level
        detail_level = meta_answers.get('detail_level', 'moderate')
        template = self.select_template(detail_level)

        # Filter questions based on preferences
        filtered_template = self.filter_questions(template, meta_answers)

        # Generate markdown
        markdown_content = self.generate_markdown(filtered_template)

        return markdown_content

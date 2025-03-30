import os
import re
import glob

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    modified_content = content
    
    modified_content = re.sub(
        r'use Sensio\\Bundle\\FrameworkExtraBundle\\Configuration\\IsGranted;',
        r'use Symfony\\Component\\Security\\Http\\Attribute\\IsGranted;',
        modified_content
    )
    
    modified_content = re.sub(
        r'use Sensio\\Bundle\\FrameworkExtraBundle\\Configuration\\Security;',
        r'use Symfony\\Component\\Security\\Http\\Attribute\\Security;',
        modified_content
    )
    
    if 'QueryParam' in modified_content and 'use FOS\\RestBundle\\Controller\\Annotations\\QueryParam;' not in modified_content:
        modified_content = re.sub(
            r'use FOS\\RestBundle\\Controller\\Annotations as Rest;',
            r'use FOS\\RestBundle\\Controller\\Annotations\\QueryParam;'
            r'\nuse FOS\\RestBundle\\Controller\\Annotations\\Get;'
            r'\nuse FOS\\RestBundle\\Controller\\Annotations\\Post;'
            r'\nuse FOS\\RestBundle\\Controller\\Annotations\\Put;'
            r'\nuse FOS\\RestBundle\\Controller\\Annotations\\Patch;'
            r'\nuse FOS\\RestBundle\\Controller\\Annotations\\Delete;'
            r'\nuse FOS\\RestBundle\\Controller\\Annotations\\View;'
            r'\nuse FOS\\RestBundle\\Controller\\Annotations\\Route as RestRoute;',
            modified_content
        )
    else:
        modified_content = re.sub(
            r'use FOS\\RestBundle\\Controller\\Annotations as Rest;',
            r'use FOS\\RestBundle\\Controller\\Annotations\\Get;'
            r'\nuse FOS\\RestBundle\\Controller\\Annotations\\Post;'
            r'\nuse FOS\\RestBundle\\Controller\\Annotations\\Put;'
            r'\nuse FOS\\RestBundle\\Controller\\Annotations\\Patch;'
            r'\nuse FOS\\RestBundle\\Controller\\Annotations\\Delete;'
            r'\nuse FOS\\RestBundle\\Controller\\Annotations\\View;'
            r'\nuse FOS\\RestBundle\\Controller\\Annotations\\Route as RestRoute;',
            modified_content
        )
    
    annotation_with_commented_method_pattern = re.compile(
        r'/\*\*\s*\n(?:\s*\*[^\n]*\n)*\s*\*\s*@Rest\\(?:Get|Post|Put|Patch|Delete|View)\([^\)]+\)[^\n]*\n(?:\s*\*[^\n]*\n)*\s*\*/\s*\n\s*/\*\s*public\s+function\s+[^{]*\{[^/]*\*/\s*',
        re.DOTALL
    )
    
    combined_commented_block_pattern = re.compile(
        r'/\*\*?\s*\n(?:\s*\*[^\n]*\n)*\s*\*\s*@Rest\\(?:Get|Post|Put|Patch|Delete|View)\([^\)]+\)[^\n]*\n(?:\s*\*[^\n]*\n)*\s*\*\s*public\s+function\s+[^{]*\{[^/]*\*/\s*',
        re.DOTALL
    )
    
    def remove_annotation_block(original_content, annotation_match):
        block = annotation_match.group(0)
        
        if re.search(r'\*\s*public\s+function', block):
            function_part = re.sub(r'/\*\*?\s*\n(?:\s*\*[^\n]*\n)*\s*\*\s*@Rest\\(?:Get|Post|Put|Patch|Delete|View)\([^\)]+\)[^\n]*\n(?:\s*\*[^\n]*\n)*', '/*', block)
            return original_content[:annotation_match.start()] + function_part + original_content[annotation_match.end():]
        else:
            method_match = re.search(r'(/\*\s*public\s+function\s+[^{]*\{[^/]*\*/\s*)', block)
            if method_match:
                return original_content[:annotation_match.start()] + method_match.group(1) + original_content[annotation_match.end():]
            else:
                return original_content[:annotation_match.start()] + original_content[annotation_match.end():]
    
    annotation_with_commented_method_matches = list(annotation_with_commented_method_pattern.finditer(modified_content))
    for match in reversed(annotation_with_commented_method_matches):
        modified_content = remove_annotation_block(modified_content, match)
    
    combined_commented_block_matches = list(combined_commented_block_pattern.finditer(modified_content))
    for match in reversed(combined_commented_block_matches):
        modified_content = remove_annotation_block(modified_content, match)
    
    commented_methods = re.finditer(r'/\*\s*public\s+function\s+(\w+)', modified_content)
    
    for method_match in commented_methods:
        method_name = method_match.group(1)
        method_pos = method_match.start()
        
        look_back = min(1000, method_pos)
        search_area = modified_content[method_pos - look_back:method_pos]
        
        annotation_match = re.search(
            r'(/\*\*\s*\n(?:\s*\*[^\n]*\n)*\s*\*\s*@Rest\\(?:Get|Post|Put|Patch|Delete|View)\([^\)]+\)[^\n]*\n(?:\s*\*[^\n]*\n)*\s*\*/)\s*(?!public\s+function)',
            search_area
        )
        
        if annotation_match:
            abs_pos = method_pos - look_back + annotation_match.start()
            modified_content = modified_content[:abs_pos] + modified_content[abs_pos + len(annotation_match.group(1)):]
    
    def process_annotations(pattern, processed_content, attribute_formatter):
        matches = list(pattern.finditer(processed_content))
        
        for match in reversed(matches):
            following_text = processed_content[match.end():match.end() + 200]
            is_for_commented_method = re.search(r'/\*\s*public\s+function', following_text)
            
            if is_for_commented_method:
                continue
                
            new_attribute = attribute_formatter(match)
            
            comment_end = processed_content.find("*/", match.end())
            if comment_end != -1:
                processed_content = processed_content[:comment_end+2] + "\n" + new_attribute + processed_content[comment_end+2:]
                processed_content = processed_content[:match.start()] + processed_content[match.end():]
        
        return processed_content
    
    isgranted_pattern = re.compile(
        r'\s*\*\s*@IsGranted\(\"([^\"]+)\"(?:,\s*message\s*=\s*\"([^\"]+)\")?\)',
        re.MULTILINE
    )
    
    def format_isgranted(match):
        role = match.group(1)
        message = match.group(2)
        
        if message:
            return f'\t#[IsGranted("{role}", message: "{message}")]'
        else:
            return f'\t#[IsGranted("{role}")]'
    
    processed_content = process_annotations(isgranted_pattern, modified_content, format_isgranted)
    
    security_pattern = re.compile(
        r'\s*\*\s*@Security\(\"([^\"]+)\"(?:,\s*message\s*=\s*\"([^\"]+)\")?\)',
        re.MULTILINE
    )
    
    def format_security(match):
        expression = match.group(1)
        message = match.group(2)
        
        if message:
            return f'\t#[Security("{expression}", message: "{message}")]'
        else:
            return f'\t#[Security("{expression}")]'
    
    processed_content = process_annotations(security_pattern, processed_content, format_security)
    
    queryparam_pattern = re.compile(
        r'\s*\*\s*@Rest\\QueryParam\(name=\"([^\"]+)\"(?:,\s*requirements=(?:\"([^\"]+)\"|(\{[^\}]+\})))?(?:,\s*default=(?:\"([^\"]+)\"|(\d+)))?(.*?)\)',
        re.MULTILINE
    )
    
    def format_queryparam(match):
        name = match.group(1)
        requirements_string = match.group(2)
        requirements_obj = match.group(3)
        default_string = match.group(4)
        default_number = match.group(5)
        other_params = match.group(6)
        
        attribute_parts = [f'name: "{name}"']
        
        if requirements_string:
            attribute_parts.append(f'requirements: "{requirements_string}"')
        elif requirements_obj:
            requirements = requirements_obj.replace('{', '[').replace('}', ']')
            requirements = re.sub(r'(\"\w+\")\s*=\s*', r'\1=>', requirements)
            attribute_parts.append(f'requirements: {requirements}')
            
        if default_string:
            attribute_parts.append(f'default: "{default_string}"')
        elif default_number:
            attribute_parts.append(f'default: {default_number}')
            
        if other_params and other_params.strip():
            other_params = other_params.strip()
            if other_params.startswith(','):
                other_params = other_params[1:].strip()
            
            reformatted_params = re.sub(r'(\w+)\s*=\s*', r'\1: ', other_params)
            reformatted_params = reformatted_params.replace('""', '"')
            
            if reformatted_params:
                attribute_parts.append(reformatted_params)
        
        return f'\t#[QueryParam({", ".join(attribute_parts)})]'
    
    processed_content = process_annotations(queryparam_pattern, processed_content, format_queryparam)
    
    rest_methods = ['Get', 'Post', 'Put', 'Patch', 'Delete', 'View']
    
    for method in rest_methods:
        rest_pattern = re.compile(
            r'\s*\*\s*@Rest\\' + method + r'\(\"([^\"]+)\"(?:,\s*name\s*=\s*\"([^\"]+)\")?(?:,\s*(.+?))?\)',
            re.MULTILINE
        )
        
        def format_rest_method(match):
            path = match.group(1)
            name = match.group(2)
            extra_params = match.group(3)
            
            attribute_params = []
            if path:
                attribute_params.append(f"'{path}'")
            if name:
                attribute_params.append(f"name: '{name}'")
                
            if extra_params:
                requirements_match = re.search(r'requirements\s*=\s*(\{.*?\})', extra_params)
                if requirements_match:
                    requirements_content = requirements_match.group(1)
                    
                    converted_requirements = requirements_content.replace('{', '[')
                    converted_requirements = converted_requirements.replace('}', ']')
                    converted_requirements = re.sub(r'(\"\w+\")\s*=\s*', r'\1=>', converted_requirements)

                    
                    attribute_params.append(f"requirements: {converted_requirements}")
                    
                    extra_params = re.sub(r'requirements\s*=\s*\{.*?\}(,\s*)?', '', extra_params)
                    extra_params = re.sub(r',\s*,', ',', extra_params)
                    extra_params = re.sub(r',\s*$', '', extra_params)
                
                if extra_params and extra_params.strip() and extra_params.strip() != ',':
                    reformatted_params = re.sub(r'(\w+)\s*=\s*', r'\1: ', extra_params)
                    attribute_params.append(reformatted_params)
            
            result = f'\t#[{method}({", ".join(attribute_params)})]'
            result = result.replace('"})]', '"])]')
 
            return result
        
        processed_content = process_annotations(rest_pattern, processed_content, format_rest_method)
    
    for method in rest_methods:
        rest_commented_pattern = re.compile(
            r'/\*\*\s*\n(?:\s*\*[^\n]*\n)*\s*\*\s*@Rest\\' + method + r'\([^\)]+\)[^\n]*\n(?:\s*\*[^\n]*\n)*\s*\*/\s*\n\s*/\*\s*',
            re.DOTALL
        )
        
        matches = list(rest_commented_pattern.finditer(processed_content))
        for match in reversed(matches):
            end_of_annotation = processed_content.find('*/', match.start()) + 2
            processed_content = processed_content[:match.start()] + processed_content[end_of_annotation:]
    
    empty_comment_pattern = re.compile(
        r'/\*\*[\s\*]*\*/',
        re.MULTILINE
    )
    
    processed_content = re.sub(empty_comment_pattern, '', processed_content)
    
    processed_content = re.sub(
        r'/\*\*\s*\n\s*\*\s*\n\s*\*/',
        '',
        processed_content
    )
    
    processed_content = re.sub(r'\n{3,}', '\n\n', processed_content)
    processed_content = re.sub(r'requirements: \[(.*?)\}\]', r'requirements: [\1]]', processed_content)
    
    orphan_rest_pattern = re.compile(
        r'/\*\*\s*\n(?:\s*\*[^\n]*\n)*\s*\*\s*@Rest\\(?:Get|Post|Put|Patch|Delete|View)\([^\)]+\)[^\n]*\n(?:\s*\*[^\n]*\n)*\s*\*/\s*(?!\s*(?:public|private|protected|#|\*/|/\*))',
        re.DOTALL
    )
    
    matches = list(orphan_rest_pattern.finditer(processed_content))
    for match in reversed(matches):
        processed_content = processed_content[:match.start()] + processed_content[match.end():]
    
    if processed_content != content:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(processed_content)
        return True
    return False

def process_file_correction(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Correction de la mauvaise transformation de : [[:xdigit:]][8], -[[:xdigit:]]{4} au lieu de : [[:xdigit:]]{8}-[[:xdigit:]]{4}
    modified_content = re.sub(
        r'\[\[:xdigit:\]\]\[8\], -\[\[:xdigit:\]\]\{4\}-\[\[:xdigit:\]\]\{4\}-\[\[:xdigit:\]\]\{4\}-\[\[:xdigit:\]\]\{12\}',
        r'[[:xdigit:]]{8}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{12}',
        content
    )

    if modified_content != content:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        return True
    return False

def main():
    controller_files = glob.glob('src/Controller/*.php', recursive=True)
    
    modified_files = 0
    for file_path in controller_files:
        if process_file(file_path):
            print(f"Modifié: {file_path}")
            modified_files += 1
    # correction requirement routes
    for file_path in controller_files:
        if process_file_correction(file_path):
            print(f"Correction: {file_path}")
    
    print(f"\nTraitement terminé. {modified_files} fichiers ont été modifiés.")

if __name__ == "__main__":
    main()

def read_classes_from_df(project_df):
    classes = []

    for _, row in project_df.iterrows():
        class_name = row['filename']
        code_imports = eval(row['code_imports']) if isinstance(row['code_imports'], str) else row['code_imports']
        imports = eval(row['imports']) if isinstance(row['imports'], str) else row['imports']
        implements = eval(row['implements']) if isinstance(row['implements'], str) else row['implements']

        classes.append({
            'class_name': class_name,
            'code_imports': code_imports,
            'imports': imports,
            'implements': implements,
            'is_main': row['is_main']
        })
        
    return classes
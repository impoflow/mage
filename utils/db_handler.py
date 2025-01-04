from mage.utils.fs_utils import read_classes_from_df

class Neo4jHandler:
    def __init__(self, connection):
        self.driver = connection._driver
    
    def close(self):
        self.driver.close()
    
    def add_user(self, name):
        query = """
        MERGE (:User {name: $name})
        """
        with self.driver.session() as session:
            session.run(query, name=name)
    
    def add_project(self, name, user):
        query = """
        MERGE (:Project {name: $name, user: $user})
        """
        with self.driver.session() as session:
            session.run(query, name=name, user=user)
    
    def create_ownership(self, user_name, project_name):
        query = """
        MATCH (u:User {name: $user_name})
        MATCH (p:Project {name: $project_name, user: $user_name})
        MERGE (u)-[:OWNS]->(p)
        """
        with self.driver.session() as session:
            session.run(query, user_name=user_name, project_name=project_name)
    
    def create_collab(self, user_name, project_name, owner):
        query = """
        MATCH (u:User {name: $user_name})
        MATCH (p:Project {name: $project_name, user: $owner})
        MERGE (u)-[:COLLABORATES_IN]->(p)
        """
        with self.driver.session() as session:
            session.run(query, user_name=user_name, project_name=project_name, owner=owner)
    
    def add_main_class(self, project_name, class_name, owner):
        query = """
        MATCH (p:Project {name: $project_name, user: $owner})
        MERGE (c:Class {name: $class_name, project: $project_name, user: $owner})
        MERGE (c)-[:MAIN]->(p)
        """
        with self.driver.session() as session:
            session.run(query, project_name=project_name, owner=owner, class_name=class_name)
    
    def add_class_node(self, class_name, project_name, owner):
        query = """
        MERGE (c:Class {name: $class_name, project: $project_name, user: $owner})
        """
        with self.driver.session() as session:
            session.run(query, class_name=class_name, project_name=project_name, owner=owner)
    
    def add_import(self, class1, class2, project_name, owner):
        query = """
        MATCH (c1:Class {name: $class1, project: $project_name, user: $owner})
        MATCH (c2:Class {name: $class2, project: $project_name, user: $owner})
        MERGE (c1)-[:IMPORTS]->(c2)
        """
        with self.driver.session() as session:
            session.run(query, class1=class1, class2=class2, project_name=project_name, owner=owner)
    
    def add_implement(self, class1, class2, project_name, owner):
        query = """
        MATCH (c1:Class {name: $class1, project: $project_name, user: $owner})
        MATCH (c2:Class {name: $class2, project: $project_name, user: $owner})
        MERGE (c1)-[:IMPLEMENTS]->(c2)
        """
        with self.driver.session() as session:
            session.run(query, class1=class1, class2=class2, project_name=project_name, owner=owner)

    def add_classes_from_csv(self, owner, project_name, data):
        classes = read_classes_from_df(data)
        for class_info in classes:
            class_name = class_info['class_name']
            imports = class_info['imports']
            implements = class_info['implements']
            
            self.add_class_node(class_name, project_name, owner)
            
            if class_name.endswith('Main'):
                self.add_main_class(project_name, class_name, owner)
            for import_class in imports:
                self.add_class_node(import_class, project_name, owner)
                self.add_import(class_name, import_class, project_name, owner)
                print(class_name, import_class)
            for implement_class in implements:
                self.add_class_node(implement_class, project_name, owner)
                self.add_implement(class_name, implement_class, project_name, owner)

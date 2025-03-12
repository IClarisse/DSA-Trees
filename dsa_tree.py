class DirectoryNode:
    def __init__(self, name):
        self.name = name
        self.children = {}  
        self.parent = None  
    
    def add_child(self, child):
        """Add a child node to this directory"""
        child.parent = self  # Set the parent reference
        self.children[child.name] = child
        print(f"Adding directory: {child.name} under {self.get_path()}")
        return child
    
    def remove_child(self, child_name):
        """Remove a child directory by name"""
        if child_name in self.children:
            print(f"Deleting directory: {child_name} and all its subdirectories from {self.get_path()}")
            del self.children[child_name]
            return True
        return False
    
    def get_child(self, child_name):
        """Get a child directory by name"""
        return self.children.get(child_name)
    
    def get_path(self):
        """Get the full path of this directory"""
        if self.parent is None:
            return self.name
        return self.parent.get_path() + '/' + self.name


class DirectoryTree:
    def __init__(self, root_name="Root"):
        self.root = DirectoryNode(root_name)
    
    def add_directory(self, path):
        """
        Add a directory at the specified path.
        Path should be in format: "dir1/dir2/dir3"
        """
        parts = path.split('/')
        current = self.root
        
        i = 0
        while i < len(parts):
            child = current.get_child(parts[i])
            if child is None:
                break
            current = child
            i += 1
        
        while i < len(parts):
            new_dir = DirectoryNode(parts[i])
            current = current.add_child(new_dir)
            i += 1
        
        return current
    
    def delete_directory(self, path):
        """
        Delete a directory at the specified path.
        Path should be in format: "dir1/dir2/dir3"
        """
        parts = path.split('/')
        if not parts:
            return False
        
        current = self.root
        for i in range(len(parts) - 1):
            child = current.get_child(parts[i])
            if child is None:
                print(f"Error: Directory '{path}' does not exist.")
                return False  # Path doesn't exist
            current = child
        
        if current.remove_child(parts[-1]):
            print(f"Successfully deleted: {path}")
            return True
        else:
            print(f"Error: Failed to delete '{path}', directory not found.")
            return False
    
    def get_directory(self, path):
        """
        Get a directory at the specified path.
        Path should be in format: "dir1/dir2/dir3"
        """
        if not path:
            return self.root
            
        parts = path.split('/')
        current = self.root
        
        for part in parts:
            child = current.get_child(part)
            if child is None:
                print(f"Error: Directory '{path}' not found.")
                return None  # Path doesn't exist
            current = child
            
        return current
    
    def list_directories(self, path="", indent=0):
        """List all directories starting from the specified path"""
        current = self.get_directory(path)
        if current is None:
            return f"Directory not found: {path}"
        
        result = []
        def _list_recursive(node, depth):
            result.append("  " * depth + node.name + "/")
            for child_name in sorted(node.children.keys()):
                _list_recursive(node.children[child_name], depth + 1)
        
        _list_recursive(current, indent)
        return "\n".join(result)


# Example usage
if __name__ == "__main__":
    # Create the directory tree
    dir_tree = DirectoryTree()
    
    # Add directories
    dir_tree.add_directory("Pictures")
    dir_tree.add_directory("Pictures/saved pictures")
    dir_tree.add_directory("Pictures/saved pictures/web images")
    dir_tree.add_directory("Pictures/saved pictures/web images/Chrome")
    dir_tree.add_directory("Pictures/saved pictures/web images/Opera")
    dir_tree.add_directory("Pictures/saved pictures/web images/Firefox")
    
    dir_tree.add_directory("Pictures/Screenshots")
    
    dir_tree.add_directory("Pictures/Camera Roll")
    dir_tree.add_directory("Pictures/Camera Roll/2025")
    dir_tree.add_directory("Pictures/Camera Roll/2024")
    dir_tree.add_directory("Pictures/Camera Roll/2023")
    
    # List directories
    print("\nInitial directory structure:")
    print(dir_tree.list_directories())
    
    print("\nAdding a new directory:")
    dir_tree.add_directory("Pictures/Camera Roll/2025/Vacation")
    print(dir_tree.list_directories())
    
    print("\nDeleting a directory:")
    dir_tree.delete_directory("Pictures/saved pictures/web images/Opera")
    print(dir_tree.list_directories())
    
    print("\nDeleting a directory and all its subdirectories:")
    dir_tree.delete_directory("Pictures/saved pictures/web images")
    print(dir_tree.list_directories())

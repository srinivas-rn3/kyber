#!/usr/bin/env python3
"""
Simple test script to verify the financial advisor bot setup
"""

def test_imports():
    """Test if all modules can be imported"""
    try:
        print("Testing imports...")
        import config as Config
        print("✅ Config imported")
        
        from load_data import load_expenses
        print("✅ load_data imported")
        
        from build_kb import build_kb
        print("✅ build_kb imported")
        
        # Don't import tools yet as it might try to load the DB
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_loading():
    """Test if CSV data can be loaded"""
    try:
        print("\nTesting data loading...")
        import config as Config
        from load_data import load_expenses
        
        docs = load_expenses(Config.KB_FILE)
        print(f"✅ Loaded {len(docs)} documents")
        if docs:
            print(f"Sample document: {docs[0].page_content[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Data loading error: {e}")
        return False

def test_kb_building():
    """Test if knowledge base can be built"""
    try:
        print("\nTesting knowledge base building...")
        from build_kb import build_kb
        
        db = build_kb()
        print("✅ Knowledge base built successfully")
        return True
    except Exception as e:
        print(f"❌ KB building error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Financial Advisor Bot Setup\n")
    
    success = True
    success &= test_imports()
    success &= test_data_loading()
    success &= test_kb_building()
    
    if success:
        print("\n🎉 All tests passed! Your bot should work correctly.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
try:
    import due_diligence_pf.wsgi
    print("Import successful")
except ImportError as e:
    print(f"Import failed: {e}")

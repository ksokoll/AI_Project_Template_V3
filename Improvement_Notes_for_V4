TODO #1: Update test conventions in AI_Project_Template_V4

Current state: all tests are flat functions with @pytest.mark decorators.
This works for the template's current size (4-5 tests per file), but does
not scale. Known disadvantages of flat test functions at project scale:

- No visual grouping in test output. With 10+ tests per file, pytest
  output becomes a flat list where happy-path and error-handling tests
  are interleaved. Classes produce nested output automatically.
- Fixture signatures repeat across every function. When five tests need
  the same three fixtures, that is five identical parameter lists.
  A class method shares setup via a helper without polluting conftest.py.
- No local namespace for test-group-specific helpers. Helpers like
  _make_classifier end up as module-level functions with no clear
  ownership. In a class, ownership is explicit.
- @pytest.mark decorators repeat on every function. With classes, one
  decorator on the class covers all methods.
- Stub duplication across files. Without classes encouraging local
  structure, the path of least resistance is to copy-paste stubs into
  each test file instead of importing from conftest.py.

The template should build for scale from the start, not refactor later.

Updated conventions:

- Group tests in classes when a test file contains more than one logical
  test group. Each class describes a behaviour, not a method.
  Name pattern: TestProcessorReturnsResult, TestProcessorErrorHandling.
- Place @pytest.mark.unit (or integration/e2e) on the class, not on
  every method. pytest inherits the marker to all methods.
- Immutable test data that requires no setup becomes a module-level
  constant (SAMPLE_REQUEST), not a fixture. Fixtures that only do
  "return SomeModel(...)" are indirection without benefit.
- Fixtures used by only one test group become helper methods on the
  class (_make_processor), not conftest.py fixtures. conftest.py is
  reserved for shared stubs and cross-file fixtures.
- Keep flat functions (no class) only when a file has a single logical
  group with fewer than five tests.

Reference: customer-support-ai refactor, reviewed 2026-03-24.

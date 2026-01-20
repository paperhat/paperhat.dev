Status: NORMATIVE
Lock State: UNLOCKED
Version: 0.1
Editor: Charles F. Munat

# Behavior Vocabulary — Text

This specification defines the **Text operator family** for the Behavior Vocabulary.

This document is **Normative**.

---

## 1. Purpose

This specification defines comprehensive text operations for Behavior Programs, including:

- Text construction and manipulation
- Character operations
- Searching and pattern matching
- Case transformation
- Unicode operations
- Encoding/decoding

---

## 2. Basic Operations (Normative)

### 2.1 Length and Size

```
TextLength(text) -> Integer
```

Returns: number of Unicode scalar values.

```
TextByteLength(text, encoding) -> Integer
```

Returns: byte length in specified encoding ("utf-8", "utf-16", "utf-32").

```
IsEmptyText(text) -> Boolean
IsNotEmptyText(text) -> Boolean
IsBlankText(text) -> Boolean
```

`IsBlankText` returns true if empty or contains only whitespace.

### 2.2 Concatenation

```
ConcatenateText(text1, text2) -> Text
ConcatenateText(text1, text2, ...) -> Text
JoinText(texts, separator) -> Text
```

### 2.3 Repetition

```
RepeatText(text, count) -> Text
```

### 2.4 Substring

```
Substring(text, startIndex) -> Text
Substring(text, startIndex, endIndex) -> Text
SubstringByLength(text, startIndex, length) -> Text
```

Indices are zero-based. Negative indices count from end.

### 2.5 Padding

```
PadStart(text, targetLength, padString) -> Text
PadEnd(text, targetLength, padString) -> Text
PadBoth(text, targetLength, padString) -> Text
```

### 2.6 Trimming

```
Trim(text) -> Text
TrimStart(text) -> Text
TrimEnd(text) -> Text
TrimCharacters(text, characters) -> Text
```

`TrimCharacters` removes specified characters from both ends.

### 2.7 Access

```
CharacterAt(text, index) -> Character
FirstCharacter(text) -> Character
LastCharacter(text) -> Character
```

Returns `<Absent/>` if index out of bounds.

---

## 3. Searching (Normative)

### 3.1 Index Finding

```
IndexOf(text, search) -> Integer
IndexOf(text, search, startIndex) -> Integer
LastIndexOf(text, search) -> Integer
LastIndexOf(text, search, startIndex) -> Integer
```

Returns -1 if not found.

```
IndicesOf(text, search) -> List<Integer>
```

Returns all occurrence positions.

### 3.2 Containment

```
ContainsSubstring(text, search) -> Boolean
StartsWithSubstring(text, prefix) -> Boolean
EndsWithSubstring(text, suffix) -> Boolean
```

### 3.3 Counting

```
CountOccurrences(text, search) -> Integer
```

---

## 4. Replacement (Normative)

### 4.1 Basic Replacement

```
ReplaceFirst(text, search, replacement) -> Text
ReplaceLast(text, search, replacement) -> Text
ReplaceAll(text, search, replacement) -> Text
```

### 4.2 Pattern Replacement

```
ReplaceFirstPattern(text, pattern, replacement) -> Text
ReplaceAllPattern(text, pattern, replacement) -> Text
```

Pattern is a regular expression per the Regular Expression Profile.

### 4.3 Character Replacement

```
ReplaceCharacters(text, fromChars, toChars) -> Text
```

Character-by-character translation (like tr).

### 4.4 Removal

```
RemoveSubstring(text, search) -> Text
RemoveAllSubstrings(text, search) -> Text
RemoveCharacters(text, characters) -> Text
```

---

## 5. Splitting and Joining (Normative)

### 5.1 Splitting

```
Split(text, separator) -> List<Text>
SplitByPattern(text, pattern) -> List<Text>
SplitByLength(text, length) -> List<Text>
SplitLines(text) -> List<Text>
SplitWords(text) -> List<Text>
```

### 5.2 Partitioning

```
Partition(text, separator) -> Tuple<Text, Text, Text>
PartitionLast(text, separator) -> Tuple<Text, Text, Text>
```

Returns: (before, separator, after). If not found, returns (text, "", "").

---

## 6. Case Transformation (Normative)

### 6.1 Standard Case

```
ToUpperCase(text) -> Text
ToLowerCase(text) -> Text
ToTitleCase(text) -> Text
```

### 6.2 Programming Case

```
ToCamelCase(text) -> Text
ToPascalCase(text) -> Text
ToSnakeCase(text) -> Text
ToKebabCase(text) -> Text
ToScreamingSnakeCase(text) -> Text
```

### 6.3 Sentence Case

```
ToSentenceCase(text) -> Text
Capitalize(text) -> Text
Uncapitalize(text) -> Text
```

`Capitalize` uppercases first character.
`Uncapitalize` lowercases first character.

### 6.4 Case Predicates

```
IsUpperCase(text) -> Boolean
IsLowerCase(text) -> Boolean
IsTitleCase(text) -> Boolean
IsMixedCase(text) -> Boolean
```

### 6.5 Case-Insensitive Comparison

```
EqualsIgnoreCase(text1, text2) -> Boolean
CompareIgnoreCase(text1, text2) -> Integer
```

`CompareIgnoreCase` returns -1, 0, or 1.

---

## 7. Pattern Matching (Normative)

### 7.1 Regular Expression Matching

```
MatchesPattern(text, pattern) -> Boolean
DoesNotMatchPattern(text, pattern) -> Boolean
```

### 7.2 Finding Matches

```
FindFirstMatch(text, pattern) -> Record { match, index, groups }
FindAllMatches(text, pattern) -> List<Record { match, index, groups }>
```

`groups` is a List of captured group strings.

### 7.3 Testing

```
TestPattern(text, pattern) -> Boolean
```

Equivalent to `MatchesPattern`.

### 7.4 Extraction

```
ExtractFirstMatch(text, pattern) -> Text
ExtractAllMatches(text, pattern) -> List<Text>
ExtractGroups(text, pattern) -> List<Text>
```

---

## 8. Character Classification (Normative)

### 8.1 Content Predicates

```
ContainsOnlyDigits(text) -> Boolean
ContainsOnlyLetters(text) -> Boolean
ContainsOnlyLettersAndDigits(text) -> Boolean
ContainsOnlyWhitespace(text) -> Boolean
ContainsOnlyAscii(text) -> Boolean
ContainsOnlyPrintable(text) -> Boolean
```

### 8.2 Character Type Counts

```
DigitCount(text) -> Integer
LetterCount(text) -> Integer
WhitespaceCount(text) -> Integer
UpperCaseCount(text) -> Integer
LowerCaseCount(text) -> Integer
```

---

## 9. Character Operations (Normative)

### 9.1 Construction

```
MakeCharacter(codePoint) -> Character
CharacterFromText(text) -> Character
```

`CharacterFromText` extracts single character. Error if text length != 1.

### 9.2 Code Point

```
CodePoint(character) -> Integer
CharacterFromCodePoint(codePoint) -> Character
```

### 9.3 Classification

```
IsLetter(character) -> Boolean
IsDigit(character) -> Boolean
IsLetterOrDigit(character) -> Boolean
IsWhitespace(character) -> Boolean
IsUpperCaseLetter(character) -> Boolean
IsLowerCaseLetter(character) -> Boolean
IsTitleCaseLetter(character) -> Boolean
IsPunctuation(character) -> Boolean
IsSymbol(character) -> Boolean
IsControl(character) -> Boolean
IsAscii(character) -> Boolean
IsPrintable(character) -> Boolean
```

### 9.4 Case Conversion

```
CharacterToUpperCase(character) -> Character
CharacterToLowerCase(character) -> Character
CharacterToTitleCase(character) -> Character
```

### 9.5 Character to Text

```
CharacterToText(character) -> Text
```

### 9.6 Type Guard

```
IsCharacter(value) -> Boolean
```

---

## 10. Unicode Operations (Normative)

### 10.1 Normalization

```
NormalizeNfc(text) -> Text
NormalizeNfd(text) -> Text
NormalizeNfkc(text) -> Text
NormalizeNfkd(text) -> Text
IsNormalized(text, form) -> Boolean
```

Forms: "NFC", "NFD", "NFKC", "NFKD".

### 10.2 Code Points

```
CodePoints(text) -> List<Integer>
TextFromCodePoints(codePoints) -> Text
```

### 10.3 Grapheme Clusters

```
GraphemeClusters(text) -> List<Text>
GraphemeClusterCount(text) -> Integer
GraphemeClusterAt(text, index) -> Text
```

### 10.4 Unicode Properties

```
UnicodeCategory(character) -> Text
UnicodeName(character) -> Text
UnicodeBlock(character) -> Text
UnicodeScript(character) -> Text
```

---

## 11. Comparison (Normative)

### 11.1 Basic Comparison

```
TextEquals(text1, text2) -> Boolean
TextCompare(text1, text2) -> Integer
```

`TextCompare` returns -1, 0, or 1 using Unicode code point order.

### 11.2 Alphabetical Comparison

```
IsAlphabeticallyBefore(text1, text2) -> Boolean
IsAlphabeticallyAfter(text1, text2) -> Boolean
IsAlphabeticallyEqual(text1, text2) -> Boolean
```

Uses NFC normalization then code point comparison.

### 11.3 Natural Sort Comparison

```
NaturalSortCompare(text1, text2) -> Integer
```

Treats embedded numbers as numeric values (e.g., "file2" < "file10").

---

## 12. Length Predicates (Normative)

```
HasLengthEqualTo(text, n) -> Boolean
HasLengthAtLeast(text, n) -> Boolean
HasLengthAtMost(text, n) -> Boolean
HasLengthBetween(text, min, max) -> Boolean
```

---

## 13. Encoding (Normative)

### 13.1 Base64

```
ToBase64(text) -> Text
FromBase64(base64Text) -> Text
ToBase64Url(text) -> Text
FromBase64Url(base64Text) -> Text
```

### 13.2 Hex

```
ToHex(text) -> Text
FromHex(hexText) -> Text
```

### 13.3 URL Encoding

```
UrlEncode(text) -> Text
UrlDecode(text) -> Text
UrlEncodeComponent(text) -> Text
UrlDecodeComponent(text) -> Text
```

### 13.4 HTML Encoding

```
HtmlEncode(text) -> Text
HtmlDecode(text) -> Text
```

---

## 14. Formatting (Normative)

### 14.1 Number Formatting

```
FormatInteger(n) -> Text
FormatNumber(n, decimalPlaces) -> Text
FormatNumberWithSeparator(n, decimalPlaces, thousandsSeparator, decimalSeparator) -> Text
```

### 14.2 Template Interpolation

```
InterpolateTemplate(template, values) -> Text
```

Template uses `{key}` or `{0}`, `{1}` placeholders.
`values` is a Record or List.

---

## 15. Validation (Normative)

### 15.1 Format Validation

```
IsValidEmail(text) -> Boolean
IsValidUrl(text) -> Boolean
IsValidIpv4(text) -> Boolean
IsValidIpv6(text) -> Boolean
IsValidUuid(text) -> Boolean
IsValidJson(text) -> Boolean
```

### 15.2 Type Guard

```
IsText(value) -> Boolean
```

---

## 16. Miscellaneous (Normative)

### 16.1 Reversing

```
ReverseText(text) -> Text
ReverseGraphemeClusters(text) -> Text
```

`ReverseText` reverses code points.
`ReverseGraphemeClusters` reverses grapheme clusters (correct for user-perceived characters).

### 16.2 Wrapping

```
WrapText(text, width) -> Text
WrapTextPreserveWords(text, width) -> Text
```

Inserts line breaks.

### 16.3 Squeezing

```
CollapseWhitespace(text) -> Text
SqueezeCharacter(text, character) -> Text
```

`CollapseWhitespace` replaces runs of whitespace with single space.
`SqueezeCharacter` replaces runs of specified character with single occurrence.

### 16.4 Conversion

```
TextToCharacterList(text) -> List<Character>
CharacterListToText(characters) -> Text
```

---

**End of Behavior Vocabulary — Text v0.1**

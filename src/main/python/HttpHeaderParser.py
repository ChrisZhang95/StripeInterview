'''
Part 1
In an HTTP request, the Accept-Language header describes the list of languages that the requester would like content to be returned in.
The header takes the form of a comma-separated list of language tags.
For example: "Accept-Language: en-US, fr-CA, fr-FR" means that the reader would accept:
  1. English as spoken in the United States (most preferred)
  2. French as spoken in Canada
  3. French as spoken in France (least preferred)
We're writing a server that needs to return content in an acceptable language for the requester, and we want to make use of this header.
Our server doesn't support every possible language that might be requested (yet!), but there is a set of languages that we do support.
Write a function that receives two arguments:
  an Accept-Language header value as a string and a set of supported languages,
  and returns the list of language tags that will work for the request.
The language tags should be returned in descending order of preference (the same order as they appeared in the header).
In addition to writing this function, you should use tests to demonstrate that it's correct, either via an existing testing system or one you create.

Examples:
  parse_accept_language(
    "en-US, fr-CA, fr-FR", # the client's Accept-Language header, a string
    ["fr-FR", "en-US"] # the server's supported languages, a set of strings
  )
  returns: ["en-US", "fr-FR"]

  parse_accept_language("fr-CA, fr-FR", ["en-US", "fr-FR"])
  returns: ["fr-FR"]

  parse_accept_language("en-US", ["en-US", "fr-CA"])
  returns: ["en-US"]

Part 2
Accept-Language headers will often also include a language tag that is not region-specific - for example, a tag of "en" means "any variant of English".
Extend your function to support these language tags by letting them match all specific variants of the language.

Examples:
  parse_accept_language("en", ["en-US", "fr-CA", "fr-FR"])
  returns: ["en-US"]

  parse_accept_language("fr", ["en-US", "fr-CA", "fr-FR"])
  returns: ["fr-CA", "fr-FR"]

  parse_accept_language("fr-FR, fr", ["en-US", "fr-CA", "fr-FR"])
  returns: ["fr-FR", "fr-CA"]

Part 3
Accept-Language headers will sometimes include a "wildcard" entry, represented by an asterisk, which means "all other languages".
Extend your function to support the wildcard entry.

Examples:
  parse_accept_language("en-US, *", ["en-US", "fr-CA", "fr-FR"])
  returns: ["en-US", "fr-CA", "fr-FR"]

  parse_accept_language("fr-FR, fr, *", ["en-US", "fr-CA", "fr-FR"])
  returns: ["fr-FR", "fr-CA", "en-US"]
'''


class HttpHeaderParser:
    def parse_accept_language(self, header, supported):
        result = []
        supported_set = set(supported)
        languages = self._parse_header(header)
        
        for lang in languages:
            if lang in supported_set:
                result.append(lang)
        
        return result
    
    def parse_accept_language2(self, header, supported):
        result = []
        lang_map = self._build_map(supported)
        
        languages = self._parse_header(header)
        for lang in languages:
            parts = lang.split('-')
            
            if len(parts) == 2:
                if parts[0] in lang_map and parts[1] in lang_map[parts[0]]:
                    result.append(lang)
                    lang_map[parts[0]].remove(parts[1])
            elif len(parts) == 1:
                if parts[0] in lang_map:
                    for country in list(lang_map[parts[0]]):
                        result.append(f"{parts[0]}-{country}")
        
        return result
    
    def parse_accept_language3(self, header, supported):
        result = []
        lang_map = self._build_map(supported)
        
        languages = self._parse_header(header)
        for lang in languages:
            parts = lang.split('-')
            
            if parts[0] == '*':
                for supported_lang in supported:
                    lang_parts = supported_lang.split('-')
                    if lang_parts[0] in lang_map and len(lang_map[lang_parts[0]]) > 0:
                        for country in lang_map[lang_parts[0]]:
                            if country == lang_parts[1]:
                                result.append(supported_lang)
                                break
            elif len(parts) == 2:
                if parts[0] in lang_map and parts[1] in lang_map[parts[0]]:
                    result.append(lang)
                    lang_map[parts[0]].remove(parts[1])
            elif len(parts) == 1:
                if parts[0] in lang_map:
                    countries = list(lang_map[parts[0]])
                    for country in countries:
                        result.append(f"{parts[0]}-{country}")
                        lang_map[parts[0]].remove(country)
        
        return result
    
    def _build_map(self, supported):
        lang_map = {}
        
        for lang in supported:
            parts = lang.split('-')
            if parts[0] not in lang_map:
                lang_map[parts[0]] = []
            lang_map[parts[0]].append(parts[1])
        
        return lang_map
    
    def _parse_header(self, header):
        result = []
        parts = header.split(',')
        for part in parts:
            result.append(part.strip())
        return result


def run():
    parser = HttpHeaderParser()
    print(parser.parse_accept_language("en-US, fr-CA, fr-FR", ["fr-FR", "en-US"]))
    print(parser.parse_accept_language("fr-CA, fr-FR", ["en-US", "fr-FR"]))
    print(parser.parse_accept_language("en-US", ["en-US", "fr-CA"]))
    
    print(parser.parse_accept_language2("en", ["en-US", "fr-CA", "fr-FR"]))
    print(parser.parse_accept_language2("fr", ["en-US", "fr-CA", "fr-FR"]))
    print(parser.parse_accept_language2("fr-FR, fr", ["en-US", "fr-CA", "fr-FR"]))
    
    print(parser.parse_accept_language3("en-US, *", ["en-US", "fr-CA", "fr-FR"]))
    print(parser.parse_accept_language3("fr-FR, fr, *", ["en-US", "fr-CA", "fr-FR"]))


if __name__ == "__main__":
    run()

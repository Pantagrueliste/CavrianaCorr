<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="tei xs"
    version="2.0">

  <!-- Output plain text (Markdown-ready) -->
  <xsl:output method="text" encoding="UTF-8"/>
  <xsl:strip-space elements="tei:*"/>

  <!-- 
      ENTRY POINT:
      Collect everything into $rawOutput, then do a regex
      to remove extra whitespace before punctuation.
  -->
  <xsl:template match="/">
    <xsl:variable name="rawOutput">
      <xsl:apply-templates select="tei:TEI"/>
    </xsl:variable>
    <!-- 
        Only remove spaces/tabs/newlines before punctuation.
        If you want to flatten line breaks entirely, adapt the pattern.
    -->
    <xsl:value-of select="replace($rawOutput, '[ \t\r\n]+([,;:\.])', '$1')"/>
  </xsl:template>

  <!-- 
      MAIN TEI TEMPLATE:
      Prints letter metadata, then applies templates to the text body.
  -->
  <xsl:template match="tei:TEI">
    <!-- Some local variables to build your archive reference -->
    <xsl:variable name="locusFrom" 
                  select="tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:msItem/tei:locus/@from"/>
    <xsl:variable name="locusTo"   
                  select="tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:msItem/tei:locus/@to"/>

    <xsl:variable name="archiveRef" as="xs:string" 
                  select="normalize-space(
                    concat(
                      tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:settlement, ' ',
                      tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:repository, ', ',
                      tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:collection, ', ',
                      tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:idno,
                      ', fols. ', $locusFrom, '-', $locusTo
                    )
                  )"/>

    <!-- Begin front matter in Markdown-like format -->
    <xsl:text>---&#10;</xsl:text>

    <!-- Title using correspDesc info -->
    <xsl:text>title: "</xsl:text>
    <xsl:value-of select="concat(
      tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/tei:persName,
      ' (',
      tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:date/@when,
      ')'
    )"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>expeditor: "</xsl:text>
    <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:persName"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>addressee: "</xsl:text>
    <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/tei:persName"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>date: "</xsl:text>
    <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:date/@when"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>placeOfOrigin: "</xsl:text>
    <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:placeName"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>archiveRef: "</xsl:text>
    <xsl:value-of select="$archiveRef"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>---&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>

    <!-- Now process the text body -->
    <xsl:apply-templates select="tei:text"/>
  </xsl:template>

  <!-- 
      TEI TEXT:
      Just apply templates recursively to children (<body>, <div>, etc.)
  -->
  <xsl:template match="tei:text">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- PAGE BREAK: Insert a bracketed note and blank lines -->
  <xsl:template match="tei:pb">
    <xsl:text>&#10;**[fol. </xsl:text>
    <xsl:value-of select="@n"/>
    <xsl:text>]**&#10;&#10;</xsl:text>
  </xsl:template>

  <!-- LINE BREAK:
       If break='no', add a dash at line's end; otherwise just a break.
  -->
  <xsl:template match="tei:lb">
    <xsl:choose>
      <xsl:when test="@break = 'no'">
        <xsl:text>-  &#10;</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>  &#10;</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- PARAGRAPH & OPENER/CLOSER/POSTSCRIPT: 
       Output blank lines after them.
  -->
  <xsl:template match="tei:p | tei:opener | tei:closer | tei:postscript">
    <xsl:apply-templates/>
    <xsl:text>&#10;&#10;</xsl:text>
  </xsl:template>

  <!-- NAMES: normalise whitespace -->
  <xsl:template match="tei:persName | tei:placeName">
    <xsl:value-of select="normalize-space(.)"/>
  </xsl:template>

  <!-- CHOICE: 
       Only show the expanded form. 
       If you prefer to keep abbr as well, adapt accordingly.
  -->
  <xsl:template match="tei:choice">
    <xsl:value-of select="tei:expan"/>
    <xsl:text> </xsl:text>
  </xsl:template>
  <xsl:template match="tei:choice/tei:abbr"/>

  <!-- UNCLEAR WORDS:
       Show them in brackets: [UNCLEAR: <text>]
       This will appear plainly in Markdown.
  -->
  <xsl:template match="tei:unclear">
    <xsl:text>[UNCLEAR: </xsl:text>
    <xsl:value-of select="."/>
    <xsl:text>]</xsl:text>
  </xsl:template>

  <!-- IGNORE <del> entirely, if you don't want deletions -->
  <xsl:template match="tei:del"/>

  <!-- ADDITIONS: just output them inline -->
  <xsl:template match="tei:add">
    <xsl:value-of select="."/>
  </xsl:template>

  <!-- NOTES:
       If you want editorial notes in brackets,
       e.g. [NOTE: ...].
  -->
  <xsl:template match="tei:note">
    <xsl:text>[NOTE: </xsl:text>
    <xsl:apply-templates/>
    <xsl:text>]</xsl:text>
  </xsl:template>

  <!-- GAPS & DAMAGES:
       Example placeholders for missing text. 
       Adjust to taste.
  -->
  <xsl:template match="tei:gap">
    <xsl:text>[missing </xsl:text>
    <xsl:value-of select="@quantity"/>
    <xsl:text> </xsl:text>
    <xsl:value-of select="@unit"/>
    <xsl:text>]</xsl:text>
  </xsl:template>

  <xsl:template match="tei:damage">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- SEG (and any unhandled element):
       Just apply templates so text children appear normally.
  -->
  <xsl:template match="tei:seg">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- FALLBACK for anything not matched above. -->
  <xsl:template match="tei:*">
    <xsl:apply-templates/>
  </xsl:template>

</xsl:stylesheet>

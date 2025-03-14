<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="tei xs"
    version="2.0">

  <!-- Output as plain text -->
  <xsl:output method="text" encoding="UTF-8"/>
  <xsl:strip-space elements="tei:*"/>

  <!-- Entry point -->
  <xsl:template match="/">
    <!-- If you really need to remove whitespace before punctuation overall, do it last:
         store the result of the main TEI template, then apply replace(). -->
    <xsl:variable name="rawOutput">
      <xsl:apply-templates select="tei:TEI"/>
    </xsl:variable>
    <xsl:value-of select="replace($rawOutput, '[ \t\r\n]+([,;:\.])', '$1')"/>
  </xsl:template>

  <!-- Main TEI template -->
  <xsl:template match="tei:TEI">
    <!-- Retrieve needed metadata: handle optional empties via string-length checks -->
    <xsl:variable name="locusFrom" select="tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:msItem/tei:locus/@from"/>
    <xsl:variable name="locusTo"   select="tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:msItem/tei:locus/@to"/>

    <xsl:variable name="archiveRef" as="xs:string" 
                  select="normalize-space(
                    concat(
                      tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:settlement, ' ',
                      tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:repository, ', ',
                      tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:collection, ', ',
                      tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:idno,
                      (  if (string-length($locusFrom) > 0 and string-length($locusTo) > 0) then
                           concat(', fols. ', $locusFrom, '-', $locusTo)
                         else ()
                      )
                    )
                  )"/>

    <xsl:text>---&#10;</xsl:text>

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

    <!-- Now output the body text -->
    <xsl:apply-templates select="tei:text"/>
  </xsl:template>

  <!-- Process the main text subtree -->
  <xsl:template match="tei:text">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- Page break insertion -->
  <xsl:template match="tei:pb">
    <xsl:text>&#10;**[fol. </xsl:text>
    <xsl:value-of select="@n"/>
    <xsl:text>]**&#10;&#10;</xsl:text>
  </xsl:template>

  <!-- Line break handling -->
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

  <!-- Paragraph-like elements -->
  <xsl:template match="tei:p | tei:opener | tei:closer">
    <xsl:apply-templates/>
    <xsl:text>&#10;&#10;</xsl:text>
  </xsl:template>

  <!-- Names -->
  <xsl:template match="tei:persName | tei:placeName">
    <xsl:value-of select="normalize-space(.)"/>
  </xsl:template>

  <!-- Expand abbreviations in <choice>, skip <abbr>. -->
  <xsl:template match="tei:choice">
    <xsl:value-of select="tei:expan"/>
    <xsl:text> </xsl:text>
  </xsl:template>
  <xsl:template match="tei:choice/tei:abbr"/>

  <!-- Ignore deletions -->
  <xsl:template match="tei:del"/>

  <!-- If <unclear>, just output the text as-is. -->
  <xsl:template match="tei:unclear">
    <xsl:value-of select="."/>
  </xsl:template>

  <!-- Additions: just output text. -->
  <xsl:template match="tei:add">
    <xsl:value-of select="."/>
  </xsl:template>

</xsl:stylesheet>

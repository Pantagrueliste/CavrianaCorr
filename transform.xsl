<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
   xmlns:tei="http://www.tei-c.org/ns/1.0"
   xmlns:xs="http://www.w3.org/2001/XMLSchema"
   exclude-result-prefixes="xs tei"
   version="2.0">
   
   <xsl:output method="text" encoding="UTF-8"/>
   
   <xsl:template match="tei:TEI">
       <xsl:apply-templates select="tei:teiHeader"/>
       <xsl:apply-templates select="tei:text"/>
   </xsl:template>
   
   <xsl:template match="tei:teiHeader">
       <xsl:value-of select="tei:fileDesc/tei:titleStmt/tei:author"/>
       <xsl:text>&#10;</xsl:text>
       <xsl:value-of select="tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:placeName"/>
       <xsl:text>&#10;</xsl:text>
       <xsl:value-of select="tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:date"/>
       <xsl:text>&#10;&#10;</xsl:text>
   </xsl:template>
   
   <xsl:template match="tei:text">
       <xsl:apply-templates/>
   </xsl:template>
   
   <xsl:template match="tei:pb">
       <xsl:text>&#10;**[fol. </xsl:text>
       <xsl:value-of select="@n"/>
       <xsl:text>]**&#10;</xsl:text>
   </xsl:template>
   
   <xsl:template match="tei:lb">
       <xsl:choose>
           <xsl:when test="@break='no'">
               <xsl:text>-</xsl:text>
               <xsl:text>  &#10;</xsl:text>
           </xsl:when>
           <xsl:otherwise>
               <xsl:text>  &#10;</xsl:text>
           </xsl:otherwise>
       </xsl:choose>
   </xsl:template>
   
   <xsl:template match="tei:p">
       <xsl:apply-templates/>
       <xsl:text>&#10;&#10;</xsl:text>
   </xsl:template>
   
   <xsl:template match="tei:opener">
       <xsl:apply-templates/>
       <xsl:text>&#10;&#10;</xsl:text>
   </xsl:template>
   
   <xsl:template match="tei:closer">
       <xsl:apply-templates/>
       <xsl:text>&#10;&#10;</xsl:text>
   </xsl:template>
   
   <xsl:template match="tei:persName | tei:placeName">
       <xsl:value-of select="."/>
   </xsl:template>
   
   <xsl:template match="tei:choice">
       <xsl:value-of select="tei:expan"/>
       <xsl:if test="following-sibling::text()[1]">
           <xsl:value-of select="following-sibling::text()[1]"/>
       </xsl:if>
   </xsl:template>
   
   <xsl:template match="tei:choice/tei:abbr"/>
   
   <xsl:template match="tei:del"/>
   
   <xsl:template match="tei:unclear">
       <xsl:value-of select="."/>
   </xsl:template>
   
   <xsl:template match="tei:add">
       <xsl:value-of select="."/>
   </xsl:template>
   
</xsl:stylesheet>

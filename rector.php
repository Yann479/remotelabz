<?php

declare(strict_types=1);

use Rector\Config\RectorConfig;
use Rector\Doctrine\Set\DoctrineSetList;
use Rector\Symfony\Set\SymfonySetList;
use Rector\TypeDeclaration\Rector\Property\TypedPropertyFromStrictConstructorRector;
use Rector\TypeDeclaration\Rector\ClassMethod\AddReturnTypeDeclarationRector;
use Rector\Php80\Rector\Class_\AnnotationToAttributeRector;
use Rector\Php80\ValueObject\AnnotationToAttribute;
use Rector\Php81\Rector\Property\ReadOnlyPropertyRector;
use Rector\TypeDeclaration\Rector\Property\AddPropertyTypeDeclarationRector;
use Rector\Doctrine\Rector\Property\CorrectDefaultTypesOnEntityPropertyRector;
use Rector\DeadCode\Rector\Property\RemoveUselessVarTagRector;

return static function (RectorConfig $rectorConfig): void {
    $rectorConfig->sets([
        DoctrineSetList::ANNOTATIONS_TO_ATTRIBUTES,
        SymfonySetList::ANNOTATIONS_TO_ATTRIBUTES,
        DoctrineSetList::DOCTRINE_ORM_29,
    ]);

    // Configuration pour convertir les annotations en attributs
    $rectorConfig->ruleWithConfiguration(AnnotationToAttributeRector::class, [
        new AnnotationToAttribute('JMS\Serializer\Annotation\Groups'),
        new AnnotationToAttribute('JMS\Serializer\Annotation\XmlRoot'),
        new AnnotationToAttribute('JMS\Serializer\Annotation\XmlAttribute'),
        new AnnotationToAttribute('JMS\Serializer\Annotation\Exclude'),
        new AnnotationToAttribute('JMS\Serializer\Annotation\MaxDepth'),
        new AnnotationToAttribute('JMS\Serializer\Annotation\VirtualProperty'),
        new AnnotationToAttribute('JMS\Serializer\Annotation\SerializedName'),
        new AnnotationToAttribute('JMS\Serializer\Annotation\Inline'),
        new AnnotationToAttribute('JMS\Serializer\Annotation'),
        new AnnotationToAttribute('Doctrine\ORM\Mapping\Column'),
        new AnnotationToAttribute('Doctrine\ORM\Mapping\JoinColumn'),
        new AnnotationToAttribute('Doctrine\ORM\Mapping'),
        new AnnotationToAttribute('Symfony\Component\Validator\Constraints'),
        new AnnotationToAttribute('Symfony\Bridge\Doctrine\Validator\Constraints'),
        new AnnotationToAttribute('JMS\Serializer\Annotation\Accessor'),
        new AnnotationToAttribute('JMS\Serializer\Annotation\XmlList'),
    ]);

    $rectorConfig->rule(TypedPropertyFromStrictConstructorRector::class);
    $rectorConfig->rule(AddReturnTypeDeclarationRector::class);
    $rectorConfig->rule(ReadOnlyPropertyRector::class);

    // Nouvelles règles pour ajouter les types de propriétés
    $rectorConfig->rule(AddPropertyTypeDeclarationRector::class);
    $rectorConfig->rule(CorrectDefaultTypesOnEntityPropertyRector::class);
    $rectorConfig->rule(RemoveUselessVarTagRector::class);
    $rectorConfig->importNames();
    $rectorConfig->importShortClasses(false);

    // conversion des annotations des interfaces
    $rectorConfig->phpstanConfig(__DIR__ . '/phpstan.neon');

    $rectorConfig->phpVersion(80100); // PHP 8.1
};
